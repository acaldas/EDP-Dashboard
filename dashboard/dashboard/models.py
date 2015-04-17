__author__ = 'Afonso'

from django.db import models


class Asset(models.Model):
    name = models.CharField(max_length=200)
    fabrication_date = models.DateField()
    panel = models.CharField(max_length=200)
    technology = models.ForeignKey(Technology)


class Technology(models.Model):
    name = models.CharField(max_length=200)
    max_lifetime = models.IntegerField()
    obsolescence_lifetime = models.IntegerField()