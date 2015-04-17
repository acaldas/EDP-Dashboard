# -*- coding: latin1 -*-

__author__ = 'Afonso'

from django.db import models


class Technology(models.Model):
    name = models.CharField(max_length=200)
    max_lifetime = models.IntegerField()
    obsolescence_lifetime = models.IntegerField()

    def __unicode__(self):
        return self.name


class Asset(models.Model):
    name = models.CharField(max_length=200)
    fabrication_date = models.IntegerField()
    panel = models.CharField(max_length=200, blank=True, null=True)
    technology = models.ForeignKey(Technology)

    def __unicode__(self):
        return self.name
