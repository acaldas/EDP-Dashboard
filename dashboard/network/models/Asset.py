# -*- coding: utf-8 -*-
__author__ = 'Afonso'

import autocomplete_light
from django.db import models
from datetime import date
from django.utils.encoding import smart_str
from algorithms.models.AssetType import GlobalParameter
from itertools import combinations, groupby
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json


class Asset(models.Model):
    name = models.CharField(max_length=200)
    sap_id = models.CharField(max_length=200, blank=True, null=True, verbose_name="SAP ID")
    fabrication_year = models.IntegerField()
    obsolescence_date = models.DateField()
    panel = models.CharField(max_length=200, blank=True, null=True)
    asset_type = models.ForeignKey('algorithms.AssetType')
    parameters = models.ManyToManyField('algorithms.Parameter', through='network.ParameterValue')
    substation = models.ForeignKey('network.Substation')

    def get_age(self):
        return date.today().year - self.fabrication_year

    def get_age_failure_probability(self):
        return self.asset_type.get_age_failure_probability(self.get_age())

    def get_max_age(self):
        return self.asset_type.technology.max_lifetime

    def get_paramaters_and_values(self):
        parameters = self.asset_type.get_parameters() + self.asset_type.get_global_parameters() \
                     + self.asset_type.get_external_factors() + self.asset_type.get_aging_parameters()
        result = dict.fromkeys(p.name for p in parameters)
        for p in parameters:
            result[p.pk] = {
                'name': p.name,
                'values': [{'id': v.id, 'value': v.value} for v in p.get_possible_correspondences()],
                'function': p.is_function()
            }
        return result

    def get_parameter_values(self, parameter_id, date=datetime.now()):
        return ParameterValue.objects.filter(asset=self, parameter_id=parameter_id, date__lte=date).all().order_by('-date')

    def get_global_parameter_info(self, parameter_id):
        return GlobalParameter.objects.filter(asset=self.asset_type, parameter_id=parameter_id).get()

    def get_fault_health_index(self, fault, date=datetime.now()):
        values = []
        for p in fault.parameter_set.all():
            p_values = self.get_parameter_values(p.pk, date)
            if self.has_value(p_values):
                values.append(p_values[0].get_health_index())

        if not values:
            return None

        return min(values)

    def get_component_health_index(self, component, global_parameters):
        hi = 0
        contribution = 0
        for p in global_parameters:
            local_weight = self.get_global_parameter_info(p.id).local_weight
            if self.has_value(p.values):
                contribution += local_weight
                hi += p.values[0].get_health_index() * local_weight/100.0

        for f in component.functions:
            component.parameters_reliability = 0
            for fault in f.faults:
                if fault.health_index is not None:
                    contribution += fault.local_weight
                    hi += fault.health_index * fault.local_weight/100.0
                    component.parameters_reliability += fault.local_weight

        component.reliability = contribution
        component.local_health_index = hi
        if not contribution:
            return 0
        return hi/contribution*100.0

    def get_health_index(self, components, global_parameters):
        hi = 0
        contribution = 0
        for p in global_parameters:
            global_weight = self.get_global_parameter_info(p.id).global_weight
            if self.has_value(p.values):
                hi += p.values[0].get_health_index() * global_weight/100.0
                contribution += global_weight

        for component in components:
            for f in component.functions:
                for fault in f.faults:
                    if fault.health_index is not None:
                        hi += fault.health_index * fault.global_weight/100.0
                        contribution += fault.global_weight

        self.reliability = contribution
        if not contribution:
            return 0
        return hi/contribution*100.0

    def get_reliability(self, components, global_parameters):
        contribution = 0
        for p in global_parameters:
            global_weight = self.get_global_parameter_info(p.id).global_weight
            if self.has_value(p.values):
                contribution += global_weight

        for component in components:
            for f in component.functions:
                for fault in f.faults:
                    if fault.health_index is not None:
                        contribution += fault.global_weight
        return contribution



    #FAILURE PROBABILITY
    def get_fault_failure_probability(self, fault, date=datetime.now()):
        health_index = fault.health_index or self.get_fault_health_index(fault, date) or 0
        age_fp = self.get_age_failure_probability() * fault.age_weight
        condition_fp = (100 - health_index) * fault.condition_weight
        external_fp = 0
        for external_factor in fault.get_external_factors():
            p = external_factor.parameter
            p_values = self.get_parameter_values(p.pk, date)

            if self.has_value(p_values):
                value = p_values[0].get_health_index()
            else:
                value = 0

            external_fp += (100.0 - value) * external_factor.local_weight * external_factor.global_weight /100.0

        return round((age_fp + condition_fp + external_fp)/100.0, 3)

    def get_asset_failure_probability(self, faults, date=datetime.now()):
        probabilities = [(f.failure_probability or self.get_fault_failure_probability(f, date))/100 for f in faults]
        n = len(probabilities)
        if n == 0:
            return None
        elif n == 1:
            probability = probabilities[0]
        elif n == 2:
            probability = (probabilities[0]+probabilities[1]) - probabilities[0]*probabilities[1]
        else:
            intersection = 0
            for a, b in combinations(probabilities, 2):
                intersection += a*b
            probability = sum(probabilities) - intersection + reduce(lambda x, y: x*y, probabilities)

        return round(probability*100, 0)




    #REMAINING LIFETIME
    def get_expected_statistic_life(self):
        return max(self.asset_type.technology.max_lifetime - self.get_age(), 0)

    def get_lifetime_reduction(self, date=datetime.now()):
        self.aging_parameters = []
        lifetime_reductions = []
        for p in self.asset_type.get_aging_parameters():
            p.values = self.get_parameter_values(p.pk, date)
            if self.has_value(p.values):
                lifetime_reductions.append(p.values[0].get_health_index())
            self.aging_parameters.append(p)

        if not len(lifetime_reductions):
            return None
        return max(lifetime_reductions)

    def get_reduced_lifetime(self, date=datetime.now()):
        return max(self.get_expected_statistic_life() - (self.get_lifetime_reduction(date) or 0), 0)

    def get_obsolescence_lifetime(self, date=datetime.now().date()):
        if type(date) == datetime:
            date = date.date()

        return max(0, Asset.num_years(date, self.obsolescence_date))

    def get_remaining_lifetime(self, date=datetime.now()):
        return min(self.get_obsolescence_lifetime(date), self.get_reduced_lifetime(date))



    def get_asset_info(self, date=datetime.now(), historic=False):

        info = {}
        faults = []
        info['global_parameters'] = list(self.asset_type.get_global_parameters())
        for p in info['global_parameters']:
            p.values = self.get_parameter_values(p.pk, date)

        info['external_factors'] = list(set(self.asset_type.get_external_factors()))
        for parameter in info['external_factors']:
            parameter.values = self.get_parameter_values(parameter.pk, date)

        info['aging_parameters'] = list(set(self.asset_type.get_aging_parameters()))
        for parameter in info['aging_parameters']:
            parameter.values = self.get_parameter_values(parameter.pk, date)

        all_parameters = []
        all_parameters.extend(info['global_parameters'])
        all_parameters.extend(info['external_factors'])
        all_parameters.extend(info['aging_parameters'])

        info['components'] = self.asset_type.component_set.all()
        for c in info['components']:
            c.num_parameters = 0
            c.functions = c.function_set.all()
            for f in c.functions:
                f.faults = f.fault_set.all()
                f.num_parameters = 0
                for fault in f.faults:
                    fault.parameters = fault.parameter_set.all()
                    for p in fault.parameters:
                        p.values = self.get_parameter_values(p.pk, date)
                        c.num_parameters += 1
                        f.num_parameters += 1
                    fault.health_index = self.get_fault_health_index(fault, date)
                    #failure probability
                    fault.failure_probability = self.get_fault_failure_probability(fault, date)
                    faults.append(fault)
                    all_parameters.extend(list(fault.parameters))
                f.health_index = sum(fault.global_weight/100*fault.health_index for fault in f.faults if fault.health_index is not None)
            c.health_index = self.get_component_health_index(c, info['global_parameters'])

            info['health_index'] = self.get_health_index(info['components'], info['global_parameters'])
            info['reliability'] = self.get_reliability(info['components'], info['global_parameters'])
            info['failure_probability'] = self.get_asset_failure_probability(faults, date)
            info['remaining_lifetime'] = self.get_remaining_lifetime(date)
            info['reduced_lifetime'] = self.get_reduced_lifetime(date)
            info['obsolescence_lifetime'] = self.get_obsolescence_lifetime()
            info['max_age'] = self.get_max_age()
            info['id'] = self.pk
            info['sap_id'] = self.sap_id
            info['name'] = self.name
            info['substation'] = self.substation
            info['substation_id'] = self.substation_id
            info['asset_type'] = self.asset_type
            info['fabrication_year'] = self.fabrication_year
            info['technology'] = self.asset_type.technology
            info['panel'] = self.panel
            info['recent_values'] = ParameterValue.objects.filter(asset=self).order_by('-date')[:10]
            all_parameters = filter(lambda x: self.has_value(x.values), all_parameters)
            info['all_parameters'] = all_parameters

            all_parameters_json = map(lambda p:{'id': p.pk, 'name': p.name, 'values': map(lambda v: {'date': str(v.date), 'hi': v.get_health_index()}, p.values)}, all_parameters)
            for parameter in all_parameters_json:
                parameter.get('values').append({'date': str(datetime.now().date()), 'hi': parameter.get('values')[0].get('hi')})

            info['all_parameters_json'] = json.dumps(all_parameters_json)

            all_parameters = ParameterValue.objects.filter(asset=self)
            all_parameters = filter(lambda x: x.has_value(), all_parameters)

            if historic:
                iter = groupby(sorted(all_parameters, key=lambda x: x.date, reverse=True), key=lambda x: x.date)
                info['historic'] = [{'date': str(date.date()), 'health_index': round(info['health_index']), 'reliability': round(info['reliability']),
                                                  'failure_probability': round(info['failure_probability']),'remaining_lifetime': round(info['remaining_lifetime'])}]
                for pdate, parameters in iter:
                    oldinfo = self.get_asset_info(pdate)
                    info['historic'].insert(0, {'date': str(pdate), 'health_index': round(oldinfo['health_index']), 'reliability': round(oldinfo['reliability']),
                                            'failure_probability': round(oldinfo['failure_probability']), 'remaining_lifetime': round(oldinfo['remaining_lifetime'])})

                info['historic_json'] = json.dumps(info['historic'])
        return info

    def __unicode__(self):
        return self.name

    @staticmethod
    def has_value(values):
        return values is not None and len(values) > 0 and values[0] is not None and values[0].get_health_index() is not None

    @staticmethod
    def yearsago(years, from_date=None):
        if from_date is None:
            from_date = datetime.now()
        return from_date - relativedelta(years=years)

    @staticmethod
    def num_years(begin, end=None):
        if end is None:
            end = datetime.now()
        num_years = int((end - begin).days / 365.25)
        if begin > Asset.yearsago(num_years, end):
            return num_years - 1
        else:
            return num_years


class ParameterValue(models.Model):
    asset = models.ForeignKey(Asset)
    parameter = models.ForeignKey('algorithms.Parameter')
    date = models.DateField(default=datetime.now)
    value_interval = models.ForeignKey('algorithms.ValueCorrespondence', blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    def get_possible_values(self):
        return self.parameter.get_possible_correspondences()

    def get_parameter_id(self):
        return self.parameter.pk

    def get_health_index(self):
        if self.parameter.function and isinstance(self.value, float):
            return self.parameter.function.predict(self.value)
        elif self.value_interval:
            return self.value_interval.health_index
        return None

    def get_warning(self):
        if self.value_interval and self.value_interval.warning:
            return self.value_interval.warning
        return None

    def get_alert(self):
        if self.value_interval and self.value_interval.alert:
            return self.value_interval.alert
        return None

    def has_value(self):
        if not self.value_interval or type(self.value_interval.health_index) != float:
            if type(self.value) != float:
                return False
        return True

    def get_value(self):
        if not self.value_interval or type(self.value_interval.health_index) != float:
            if type(self.value) != float:
                return 'Desconhecido'
            return str(self.value).decode('utf-8')
        return str(self.value_interval).decode('utf-8')

    def __unicode__(self):

        return str(self.parameter).decode('utf-8') + ' - ' + self.get_value()


class AssetAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^name', 'sap_id']

autocomplete_light.register(Asset, AssetAutocomplete)