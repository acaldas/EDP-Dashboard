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

    technology = models.ForeignKey(Technology)
    aging_function = models.ForeignKey('utils.RegressionFunction', null=True)

    def __unicode__(self):
        return self.name

    #FAILURE PROBABILITY
    def get_age_failure_probability(self, age):
        return self.aging_function.predict(self.get_age())


