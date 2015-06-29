# -*- coding: latin1 -*-
__author__ = 'Afonso'
import autocomplete_light
from django.db import models
from geoposition.fields import GeopositionField


class Substation(models.Model):
    name = models.CharField(max_length=200, verbose_name=u'Instalação')
    position = GeopositionField(verbose_name="Coordenadas")
    sap_id = models.CharField(max_length=200, blank=True, null=True, verbose_name="SAP ID")
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name="Morada")
    postal_code = models.CharField(max_length=200, blank=True, null=True, verbose_name="C.P.")
    ga = models.CharField(max_length=200, blank=True, null=True, verbose_name="GA")

    class Meta:
        verbose_name = u'Subestação'
        verbose_name_plural = u'Subestações'
        ordering = ['position', 'name']

    def get_assets_info(self):
        assets = []

        for asset in self.asset_set.all():
            assets.append(asset.get_asset_info())
        return assets

    @staticmethod
    def get_center_latitude():
        return 41.08707222222223

    @staticmethod
    def get_center_longitude():
        return -7.885806980884584

    def __unicode__(self):
        return u'{}'.format(self.name)


class SubstationAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^name', 'sap_id']

autocomplete_light.register(Substation, SubstationAutocomplete)