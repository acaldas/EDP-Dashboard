# -*- coding: latin1 -*-
__author__ = 'Afonso'

from django.db import models
from Component import Component


class Function(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'Nome')
    component = models.ForeignKey(Component, verbose_name=u'Componente')

    class Meta:
        verbose_name = u'Função'
        verbose_name_plural = u'Funções'

    def __unicode__(self):
        return self.name

    def get_health_index_contribution(self):
        faults = self.fault_set.all()
        return sum(f.local_weight for f in faults)

    def get_local_health_index_sum(self):
        faults = self.fault_set.all()
        return sum(f.local_weight*f.get_health_index() for f in faults)/100

    def get_global_health_index_sum(self):
        faults = self.fault_set.all()
        return sum(f.global_weight*f.get_health_index() for f in faults)/100

    def get_global_weight(self):
        faults = self.fault_set.all()
        return sum(f.global_weight for f in faults if f.get_min_parameter() is not None)

    def get_alerts(self):
        faults = self.fault_set.all()
        return sum([f.get_alerts() for f in faults], [])

    def get_warnings(self):
        faults = self.fault_set.all()
        return sum([f.get_warnings() for f in faults], [])