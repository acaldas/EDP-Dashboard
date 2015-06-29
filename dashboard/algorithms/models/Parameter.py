# -*- coding: latin1 -*-
__author__ = 'Afonso'

from django.db import models
from Fault import Fault, ExternalFactor
from AssetType import Technology, GlobalParameter


class Parameter(models.Model):

    name = models.CharField(max_length=200, verbose_name=u'Nome')
    fault = models.ForeignKey(Fault, blank=True, null=True, editable=False, verbose_name=u'Falha')
    function = models.ForeignKey('utils.RegressionFunction', null=True, blank=True, verbose_name=u'Fun��o de Regress�o')
    technology = models.ForeignKey(Technology, related_name="aging_parameters", null=True, blank=True, editable=False, verbose_name=u'Tecnologia')

    class Meta:
        verbose_name = u'Par�metro'
        verbose_name_plural = u'Par�metros'

    def __unicode__(self):
        return u'{} - {} - {}'.format(self.get_asset(), self.get_type(), self.name)

    def get_possible_correspondences(self):
        return self.valuecorrespondence_set.all()

    def get_value_correspondent(self, value):
        value_correspondences = self.valuecorrespondence_set.all()
        if len(value_correspondences) == 0:
            print "No value correspondences have been defined"
            raise Exception
        correspondences = filter(lambda x: x.check_correspondence(value), value_correspondences)
        if len(correspondences) == 0:
            print "{}:{} No correspondence".format(self.name, value)
            raise Exception
        elif len(correspondences) > 1:
            print correspondences[0].value
            print correspondences[1].value
            print "Multiple correspondence {}".format(filter(lambda x: x.value, correspondences))
            raise Exception
        else:
            return correspondences[0]

    def is_function(self):
        return self.function is not None

    def get_health_index(self, value):
        if value is None:
            return 0
        if not self.function:
            return self.get_value_correspondent(value).health_index
        return self.function.predict(value)

    def get_alert(self, value):
        return self.get_value_correspondent(value).alert

    def get_warning(self, value):
        print self.get_value_correspondent(value).warning
        return self.get_value_correspondent(value).warning

    def get_sum(self, value):
        return self.get_health_index(value)/100.0

    def save(self, *args, **kwargs):
        if isinstance(self.name, str):
            self.name = self.name.decode("utf-8")
        super(Parameter, self).save(*args, **kwargs)

    def get_asset(self):
        if self.fault and self.fault.function and self.fault.function.component and self.fault.function.component.asset:
            return self.fault.function.component.asset.name
        elif self.technology:
            return self.technology.name

        global_parameter = GlobalParameter.objects.filter(parameter=self).first()
        if global_parameter:
            return global_parameter.asset.name

        externalFactor = ExternalFactor.objects.filter(parameter=self).first()
        if externalFactor:
            return externalFactor.fault.function.component.asset.name

        return '---'

    def get_type(self):
        if self.fault and self.fault.function and self.fault.function.component and self.fault.function.component.asset:
            return u'�ndice de Sa�de'
        elif self.technology:
            return 'Envelhecimento'

        global_parameter = GlobalParameter.objects.filter(parameter=self).first()
        if global_parameter:
            return u'�ndice de Sa�de'

        externalFactor = ExternalFactor.objects.filter(parameter=self).first()
        if externalFactor:
            return 'Fator Externo'

        return '---'


class ValueCorrespondence(models.Model):
    parameter = models.ForeignKey(Parameter, verbose_name=u'Par�metro')
    value = models.CharField(max_length=200, verbose_name=u'Valor')
    health_index = models.FloatField(verbose_name=u'�ndice de Sa�de')
    warning = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'Aviso')
    alert = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'Alarme')

    class Meta:
        verbose_name = u'Correspond�ncia de Valor'
        verbose_name_plural = u'Correspond�ncias de Valor'

    def __unicode__(self):
        return u'{0}'.format(self.value)

    def check_correspondence(self, value):
        return self.value == value

    def save(self, *args, **kwargs):
        if isinstance(self.value, str):
            self.value = self.value.decode("utf-8")
        super(ValueCorrespondence, self).save(*args, **kwargs)


class Parameters(Parameter):
    class Meta:
        proxy = True
        verbose_name = u'Par�meto'
        verbose_name_plural = u'Par�metros'
        ordering = ('name',)