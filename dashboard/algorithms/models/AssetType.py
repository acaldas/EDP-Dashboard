# -*- coding: latin1 -*-

__author__ = 'Afonso'

from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'Nome')
    max_lifetime = models.IntegerField(verbose_name=u'Tempo de vida máxima')

    class Meta:
        verbose_name = "Tecnologia"
        verbose_name_plural = "Tecnologias"
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class AssetType(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'Nome')
    global_parameters = models.ManyToManyField('algorithms.Parameter', through='algorithms.GlobalParameter', verbose_name=u'Parâmetros Globais')
    technology = models.OneToOneField(Technology, verbose_name=u'Tecnologia')
    aging_function = models.ForeignKey('utils.RegressionFunction', null=True, verbose_name=u'Função de Envelhecimento')

    class Meta:
        verbose_name = "Tipo de Ativo"
        verbose_name_plural = "Tipos de Ativo"

    def __unicode__(self):
        return u'{}'.format(self.name)

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

    #REMAINING LIFETIME
    def get_aging_parameters(self):
        return list(self.technology.aging_parameters.all())


class GlobalParameter(models.Model):
    asset = models.ForeignKey(AssetType, verbose_name=u'Ativo')
    parameter = models.ForeignKey('algorithms.Parameter', verbose_name=u'Parâmetro')
    local_weight = models.FloatField(verbose_name=u'Peso Específico')
    global_weight = models.FloatField(verbose_name=u'Peso Global')

    class Meta:
        verbose_name = u"Parâmetro Global"
        verbose_name_plural = u"Parâmetros Globais"

    def __unicode__(self):
        return u'{} - {}'.format(self.asset, self.parameter.name)