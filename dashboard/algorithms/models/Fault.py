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

    def __unicode__(self):
        return self.name