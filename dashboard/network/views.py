from django.shortcuts import render
from django.http import JsonResponse
from models.Asset import Asset
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404


def home(request):
    return render(request, 'home.html')


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
    context = {'asset': asset.get_asset_info()}
    return render(request,'show_asset.html', context)


def show_asset_skeleton(request, asset_id):
    asset = get_object_or_404(Asset, pk=asset_id)
    context = {'asset': asset.get_asset_info()}
    return render(request,'show_asset_skeleton.html', context)