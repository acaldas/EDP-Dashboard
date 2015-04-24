__author__ = 'Afonso'

from django.db import models
from datetime import date


class Asset(models.Model):
    name = models.CharField(max_length=200)
    fabrication_date = models.IntegerField()
    panel = models.CharField(max_length=200, blank=True, null=True)
    asset_type = models.ForeignKey('algorithms.AssetType')

    def get_age(self):
        return date.today().year - self.fabrication_date

    def get_age_failure_probability(self):
        return self.asset_type.aging_function.predict(self.get_age())

    def __unicode__(self):
        return self.name


class ParameterValue(models.Model):
    asset = models.ForeignKey(Asset)
    parameter = models.ForeignKey('algorithms.Parameter')
    date = models.DateField()
    value = models.CharField(max_length=200)