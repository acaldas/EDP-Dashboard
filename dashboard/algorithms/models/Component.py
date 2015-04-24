__author__ = 'Afonso'

from django.db import models
from AssetType import AssetType


class Component(models.Model):
    name = models.CharField(max_length=200)
    asset = models.ForeignKey(AssetType)

    def __unicode__(self):
        return self.name

    def get_global_weight(self):
        functions = self.function_set.all()
        return sum(f.get_global_weight() for f in functions)

    def get_global_health_index_sum(self):
        functions = self.function_set.all()
        return sum(f.get_global_health_index_sum() for f in functions)

    def get_alerts(self):
        functions = self.function_set.all()
        return sum([f.get_alerts() for f in functions], [])

    def get_warnings(self):
        functions = self.function_set.all()
        return sum([f.get_warnings() for f in functions], [])