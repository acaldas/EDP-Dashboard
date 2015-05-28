__author__ = 'Afonso'
# -*- coding: utf-8 -*-

from django.db import models
from datetime import date
from django.utils.encoding import smart_str
from algorithms.models.AssetType import GlobalParameter
from itertools import combinations



class Asset(models.Model):
    name = models.CharField(max_length=200)
    fabrication_year = models.IntegerField()
    obsolescence_lifetime = models.IntegerField()
    panel = models.CharField(max_length=200, blank=True, null=True)
    asset_type = models.ForeignKey('algorithms.AssetType')
    parameters = models.ManyToManyField('algorithms.Parameter', through='network.ParameterValue')

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
            result[p.name] = {
                'values': [{'id': v.id, 'value': v.value} for v in p.get_possible_correspondences()],
                'function': p.is_function()
            }
        return result

    def get_parameter_values(self, parameter_id):
        return ParameterValue.objects.filter(asset=self, parameter_id=parameter_id).all().order_by('date')

    def get_global_parameter_info(self, parameter_id):
        return GlobalParameter.objects.filter(asset=self.asset_type, parameter_id=parameter_id).get()

    def get_fault_health_index(self, fault):
        values = []
        for p in fault.parameter_set.all():
            p_values = self.get_parameter_values(p.pk)
            if p_values is not None and p_values[0] is not None and p_values[0].get_health_index() is not None:
                values.append(p_values[0].get_health_index())
            else:
                return None
        if not values:
            return None

        return min(values)



    #FAILURE PROBABILITY
    def get_fault_failure_probability(self, fault):
        fault.health_index or self.get_fault_health_index(fault) or 0
        age_fp = self.get_age_failure_probability() * fault.age_weight
        condition_fp = (100 - fault.health_index) * fault.condition_weight
        external_fp = 0
        for external_factor in fault.get_external_factors():
            p = external_factor.parameter
            p_values = self.get_parameter_values(p.pk)

            if p_values is not None and p_values[0] is not None and p_values[0].get_health_index() is not None:
                value = p_values[0].get_health_index()
            else:
                value = 0

            external_fp += (100.0 - value) * external_factor.local_weight * external_factor.global_weight

        return round((age_fp + condition_fp + external_fp)/100.0, 3)

    def get_asset_failure_probability(self, faults):
        probabilities = [(f.failure_probability or self.get_fault_failure_probability(f))/100 for f in faults]
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

    def get_component_health_index(self, component):
        hi = 0
        contribution = 0
        for p in self.global_parameters:
            global_weight = self.get_global_parameter_info(p.id).global_weight
            if p.values and p.values[0] is not None and p.values[0].get_health_index() is not None:
                contribution += global_weight
                hi += p.values[0].get_health_index() * global_weight/100.0

        for f in component.functions:
            component.parameters_reliability = 0
            for fault in f.faults:
                if fault.health_index is not None:
                    contribution += fault.global_weight
                    hi += fault.health_index * fault.global_weight/100.0
                    component.parameters_reliability += fault.global_weight

        component.reliability = contribution
        component.global_health_index = hi
        return hi/contribution*100.0

    def get_health_index(self, components):
        hi = 0
        contribution = 0
        for p in self.global_parameters:
            global_weight = self.get_global_parameter_info(p.id).global_weight
            if p.values and p.values[0] is not None and p.values[0].get_health_index() is not None:
                hi += p.values[0].get_health_index() * global_weight/100.0
                contribution += global_weight
                print "{}:{}".format(p.name, global_weight)

        for component in components:
            hi += component.global_health_index
            contribution += component.parameters_reliability
            print "{}:{}".format(component.name, component.parameters_reliability)

        self.reliability = contribution
        return hi/contribution*100.0

    #REMAINING LIFETIME
    def get_expected_statistic_life(self):
        return max(self.asset_type.technology.max_lifetime - self.get_age(), 0)

    def get_lifetime_reduction(self):
        lifetime_reductions = []
        for p in self.asset_type.get_aging_parameters():
            p.values = self.get_parameter_values(p.pk)
            if p.values and p.values[0] is not None and p.values[0].get_health_index() is not None:
                lifetime_reductions.append(p.values[0].get_health_index())

        if not len(lifetime_reductions):
            return None
        return max(lifetime_reductions)

    def get_reducted_lifetime(self):
        return max(self.get_expected_statistic_life() - (self.get_lifetime_reduction() or 0), 0)

    def get_remaining_lifetime(self):
        return min(self.obsolescence_lifetime, self.get_reducted_lifetime())

    def get_asset_info(self):
        faults = []
        self.global_parameters = self.asset_type.get_global_parameters()
        for p in self.global_parameters:
            p.values = self.get_parameter_values(p.pk)

        self.components = self.asset_type.component_set.all()
        for c in self.components:
            c.num_parameters = 0
            c.functions = c.function_set.all()
            for f in c.functions:
                f.faults = f.fault_set.all()
                f.num_parameters = 0
                for fault in f.faults:
                    fault.parameters = fault.parameter_set.all()
                    for p in fault.parameters:
                        p.values = self.get_parameter_values(p.pk)
                        c.num_parameters += 1
                        f.num_parameters += 1
                    fault.health_index = self.get_fault_health_index(fault)
                    #failure probability
                    fault.failure_probability = self.get_fault_failure_probability(fault)
                    faults.append(fault)
                f.health_index = sum(fault.global_weight/100*fault.health_index for fault in f.faults if fault.health_index is not None)
            c.health_index = self.get_component_health_index(c)

            self.health_index = self.get_health_index(self.components)
            self.failure_probability = self.get_asset_failure_probability(faults)
            self.remaining_lifetime = self.get_remaining_lifetime()
        return self

    def __unicode__(self):
        return self.name


class ParameterValue(models.Model):
    asset = models.ForeignKey(Asset)
    parameter = models.ForeignKey('algorithms.Parameter')
    date = models.DateField()
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

    def __unicode__(self):
        if not self.value_interval:
            if not self.value:
                return '-----'
            return str(self.parameter).decode('utf-8') + ' - ' + str(self.value).decode('utf-8')
        return str(self.parameter).decode('utf-8') + ' - ' + str(self.value_interval).decode('utf-8')