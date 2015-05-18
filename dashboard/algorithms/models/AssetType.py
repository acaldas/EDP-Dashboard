# -*- coding: latin1 -*-

__author__ = 'Afonso'

from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=200)
    max_lifetime = models.IntegerField()
    obsolescence_lifetime = models.IntegerField()

    class Meta:
        verbose_name_plural = "Technologies"

    def __unicode__(self):
        return self.name


class AssetType(models.Model):
    name = models.CharField(max_length=200)
    global_parameters = models.ManyToManyField('algorithms.Parameter', through='algorithms.GlobalParameter')
    technology = models.ForeignKey(Technology)
    aging_function = models.ForeignKey('utils.RegressionFunction', null=True,)

    def __unicode__(self):
        return self.name

    def get_parameters(self):
        parameters = []
        for c in self.component_set.all():
            for f in c.function_set.all():
                for fault in f.fault_set.all():
                    for p in fault.parameter_set.all():
                        parameters.append(p)

        return parameters

    def get_global_parameters(self):
        return list(self.global_parameters.all())

    def get_external_factors(self):
        from Fault import ExternalFactor
        return list([e.parameter for e in ExternalFactor.objects.filter(fault__function__component__asset=self)])

    #FAILURE PROBABILITY
    def get_age_failure_probability(self, age):
        return self.aging_function.predict(age)


class GlobalParameter(models.Model):
    asset = models.ForeignKey(AssetType)
    parameter = models.ForeignKey('algorithms.Parameter')
    local_weight = models.FloatField()
    global_weight = models.FloatField()