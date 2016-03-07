from django.conf.urls import include, url, patterns
from django.contrib import admin
from network import views

urlpatterns = [
    # Examples:
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url('autocomplete/asset/$', views.AssetAutocomplete.as_view(), name='asset-autocomplete'),
    url('autocomplete/substation/$', views.SubstationAutocomplete.as_view(), name='substation-autocomplete'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^asset_parameters/(?P<asset_id>[0-9]+)/$', views.get_asset_parameters_and_possible_values, name = 'get_asset_parameters_and_possible_values' ),
    url(r'^asset/(?P<asset_id>[0-9]+)/$', views.show_asset, name='show_asset'),
    url(r'^asset_skeleton/(?P<asset_id>[0-9]+)/$', views.show_asset_skeleton, name='show_asset_skeleton'),
    url(r'^substation/(?P<substation_id>[0-9]+)/$', views.show_substation, name="show_substation"),
    url(r'^$', views.home, name="home"),
]
