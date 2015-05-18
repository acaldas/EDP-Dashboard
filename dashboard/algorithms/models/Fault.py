__author__ = 'Afonso'

from django.db import models
from Function import Function


class Fault(models.Model):
    name = models.CharField(max_length=200)
    function = models.ForeignKey(Function)
    global_weight = models.FloatField()
    local_weight = models.FloatField()
    condition_weight = models.FloatField()
    age_weight = models.FloatField()
    external_factors = models.ManyToManyField('algorithms.Parameter', through='algorithms.ExternalFactor', related_name='external_factors')

    def get_external_factors(self):
        #return list(self.external_factors.all())
        return list(ExternalFactor.objects.filter(fault=self))
    def __unicode__(self):
        return self.name


class ExternalFactor(models.Model):
    fault = models.ForeignKey(Fault)
    parameter = models.ForeignKey('algorithms.Parameter')
    local_weight = models.FloatField()
    global_weight = models.FloatField()


class Faults(Fault):
    class Meta:
        proxy = True
        verbose_name_plural = "Faults"