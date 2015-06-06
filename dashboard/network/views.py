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
    map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))


def home(request):

    gmap = maps.Map(opts={
        'center': maps.LatLng(Substation.get_center_latitude(), Substation.get_center_longitude()),
        'mapTypeId': maps.MapTypeId.HYBRID,
        'zoom': 8,
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

    context = {'form': MapForm(initial={'map': gmap})}
    return render_to_response('home.html', context)


def show_substation(request, substation_id):
    substation = get_object_or_404(Substation, pk=substation_id)
    context = {'substation': substation}
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
    context = {'asset': asset.get_asset_info(historic=True)}
    return render(request,'show_asset.html', context)


def show_asset_skeleton(request, asset_id):
    asset = get_object_or_404(Asset, pk=asset_id)
    context = {'asset': asset.get_asset_info(historic=True)}
    return render(request,'show_asset_skeleton.html', context)