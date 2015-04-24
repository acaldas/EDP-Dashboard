from django.contrib import admin
from django import forms
from models.Asset import Asset, ParameterValue
from algorithms.models.Parameter import Parameter


class ParameterValueInline(admin.TabularInline):
    model = ParameterValue

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(ParameterValueInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'parameter':
            if request._obj_ is not None:
                possible_parameters = map(lambda x: x.pk, request._obj_.asset_type.get_parameters())
                field.queryset = field.queryset.filter(pk__in=possible_parameters)
            else:
                field.queryset = field.queryset.none()

        return field


class AssetAdmin(admin.ModelAdmin):
    inlines = [
        ParameterValueInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(AssetAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(Asset, AssetAdmin)
