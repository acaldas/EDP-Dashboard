# -*- coding: latin1 -*-
__author__ = 'Afonso'

from django.db import models
from Function import Function


class Fault(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'Nome')
    function = models.ForeignKey(Function, verbose_name=u'Função')
    global_weight = models.FloatField(verbose_name=u'Peso Global')
    local_weight = models.FloatField(verbose_name=u'Peso Específico')
    condition_weight = models.FloatField(verbose_name=u'Peso Condição')
    age_weight = models.FloatField(verbose_name=u'Peso Idade')
    external_factors = models.ManyToManyField('algorithms.Parameter', through='algorithms.ExternalFactor', related_name='external_factors', verbose_name=u'Fatores Externos')

    class Meta:
        verbose_name = u'Falha'
        verbose_name_plural = u'Falhas'

    def get_external_factors(self):
        #return list(self.external_factors.all())
        return list(ExternalFactor.objects.filter(fault=self))

    def __unicode__(self):
        return self.name


class ExternalFactor(models.Model):

    class Meta:
        verbose_name = u'Fator Externo'
        verbose_name_plural = u'Fatores Externos'

    fault = models.ForeignKey(Fault, verbose_name=u'Falha')
    parameter = models.ForeignKey('algorithms.Parameter', verbose_name=u'Parâmetro')
    local_weight = models.FloatField(verbose_name=u'Peso Específico')
    global_weight = models.FloatField(verbose_name=u'Peso Global')


class Faults(Fault):
    class Meta:
        proxy = True
        verbose_name = u'Falhas'
        verbose_name_plural = u'Falhas'