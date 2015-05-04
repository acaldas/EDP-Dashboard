__author__ = 'Afonso'
# -*- coding: utf-8 -*-

from django.db import models
from datetime import date
from django.utils.encoding import smart_str

class Asset(models.Model):
    name = models.CharField(max_length=200)
    fabrication_date = models.IntegerField()
    panel = models.CharField(max_length=200, blank=True, null=True)
    asset_type = models.ForeignKey('algorithms.AssetType')
    parameters = models.ManyToManyField('algorithms.Parameter', through='network.ParameterValue')

    def get_age(self):
        return date.today().year - self.fabrication_date

    def get_age_failure_probability(self):
        return self.asset_type.aging_function.predict(self.get_age())

    def __unicode__(self):
        return self.name

    def get_paramaters_and_values(self):
        parameters = self.asset_type.get_parameters() + self.asset_type.get_global_parameters()
        result = dict.fromkeys(p.name for p in parameters)
        for p in parameters:
            result[p.name] = [{'id': v.id, 'value': v.value} for v in p.get_possible_correspondences()]

        return result

    def get_parameter_values(self, parameter_id):
        return ParameterValue.objects.filter(asset=self, parameter_id=parameter_id).all().order_by('date')

    def get_fault_health_index(self, fault):
        values = []
        for p in fault.parameter_set.all():
            p_values = self.get_parameter_values(p.pk)
            if p_values is not None and p_values[0] is not None and p_values[0].get_health_index() is not None:
                values.append(p_values[0].get_health_index())
        if not values:
            return 0 #TODO CHECK THIS, SHOULD BE NONE

        return min(values)

    def get_asset_info(self):
        self.components = self.asset_type.component_set.all()
        for c in self.components:
            c.functions = c.function_set.all()
            for f in c.functions:
                f.faults = f.fault_set.all()
                for fault in f.faults:
                    fault.parameters = fault.parameter_set.all()
                    for p in fault.parameters:
                        p.values = self.get_parameter_values(p.pk)

                    fault.health_index = self.get_fault_health_index(fault)

                f.health_index = sum(fault.global_weight/100*fault.health_index for fault in f.faults)
        self.global_parameters = self.asset_type.get_global_parameters()
        for p in self.global_parameters:
            p.values = self.get_parameter_values(p.pk)
        return self


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