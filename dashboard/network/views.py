# -*- coding: latin1 -*-
from django.shortcuts import render
from django import forms
from django.shortcuts import render_to_response
from django.http import JsonResponse
from models.Asset import Asset
from models.Substation import Substation
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404
from gmapi import maps
from gmapi.forms.widgets import GoogleMap


class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width': 700, 'height': 800}))


class SmallMapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width': 300, 'height': 300}))


def get_map(request, latitude=Substation.get_center_latitude(), longitude=Substation.get_center_longitude(), zoom=8):

    gmap = maps.Map(opts={
        'center': maps.LatLng(latitude, longitude),
        'mapTypeId': maps.MapTypeId.HYBRID,
        'zoom': zoom,
        'mapTypeControlOptions': {
            'style': maps.MapTypeControlStyle.DEFAULT
        },
    })

    substations = Substation.objects.all()

    substation_url = 'http://' + request.get_host() + '/substation/'

    for substation in substations:
        marker = maps.Marker(opts={'map': gmap, 'position': maps.LatLng(substation.position.latitude,
                                                                        substation.position.longitude), })
        marker.setTitle(substation_url + str(substation.pk))
        maps.event.addListener(marker, 'click', 'marker.markerClick')
        maps.event.addListener(marker, 'mouseover', 'marker.markerOver')
        maps.event.addListener(marker, 'mouseout', 'marker.markerOut')
        info = maps.InfoWindow({'content': substation.name, 'disableAutoPan': True})
        info.open(gmap, marker)

    return gmap


def home(request):
    map_form = MapForm(initial={'map': get_map(request)})
    substations = Substation.objects.order_by('-position').all()
    #assets = sorted(reduce(lambda a, b: a+b, map(lambda x: x.get_assets_info(), substations)), key=lambda x: x.get('failure_probability'), reverse=True)[0:10]
    assets = reduce(lambda a, b: a+b, map(lambda x: x.get_assets_info(), substations))
    assets.append({
        'sap_id': 280202124,
        'asset_type': u'Disjuntor - Óleo',
        'name': u'Disjuntor Óleo',
        'health_index': 43,
        'failure_probability': 78,
        'remaining_lifetime': 5,
        'max_age':30
    })
    assets.append({
        'sap_id': 280202126,
        'asset_type': u'Disjuntor - Vácuo',
        'name': u'Disjuntor Vácuo',
        'health_index': 70,
        'failure_probability': 34,
        'remaining_lifetime': 18,
        'max_age':30
    })
    assets.append({
        'sap_id': 280202125,
        'asset_type': u'Disjuntor - SF6',
        'name': u'Disjuntor SF6',
        'health_index': 82,
        'failure_probability': 24,
        'remaining_lifetime': 23,
        'max_age': 30
    })
    assets = sorted(assets,key=lambda x: x.get('failure_probability'), reverse=True)[0:10]
    context = {'form': map_form, 'substations': substations, 'assets': assets}
    return render(request, 'home.html', context)


def show_substation(request, substation_id):
    substations = Substation.objects.order_by('-position').all()
    substation = get_object_or_404(Substation, pk=substation_id)
    map_form = SmallMapForm(initial={'map': get_map(request, substation.position.latitude, substation.position.longitude, zoom=15)})
    assets = substation.get_assets_info()
    assets.append({
        'sap_id': 280202124,
        'asset_type': u'Disjuntor - Óleo',
        'name': u'Disjuntor Óleo',
        'health_index': 43,
        'failure_probability': 78,
        'remaining_lifetime': 5,
        'max_age':30
    })
    assets.append({
        'sap_id': 280202126,
        'asset_type': u'Disjuntor - Vácuo',
        'name': u'Disjuntor Vácuo',
        'health_index': 70,
        'failure_probability': 34,
        'remaining_lifetime': 18,
        'max_age':30
    })
    assets.append({
        'sap_id': 280202125,
        'asset_type': u'Disjuntor - SF6',
        'name': u'Disjuntor SF6',
        'health_index': 82,
        'failure_probability': 24,
        'remaining_lifetime': 23,
        'max_age': 30
    })
    assets = sorted(assets,key=lambda x: x.get('health_index'), reverse=True)[0:10]
    context = {'substation': substation,
               'map': map_form,
               'substations': substations,
               'assets': assets
              }
    return render(request, 'show_substation.html', context)


def get_asset_parameters_and_possible_values(request, asset_id):
    asset = Asset.objects.get(pk= asset_id)
    return JsonResponse(asset.get_paramaters_and_values())


def asset_change_form(request):
    return render_to_response(
        "report.html",
        {'asset_list': Asset.objects.all()},
        RequestContext(request, {}),
    )


def show_asset(request, asset_id):
    asset = get_object_or_404(Asset, pk=asset_id)
    substations = Substation.objects.order_by('-position').all()
    context = {'asset': asset.get_asset_info(historic=True),
               'substations': substations}
    return render(request,'show_asset.html', context)


def show_asset_skeleton(request, asset_id):
    asset = get_object_or_404(Asset, pk=asset_id)
    context = {'asset': asset.get_asset_info(historic=True)}
    return render(request,'show_asset_skeleton.html', context)