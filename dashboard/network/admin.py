from django.contrib import admin
from django import forms
import json
from models.Asset import Asset, ParameterValue
from algorithms.models.Parameter import Parameter, ValueCorrespondence


class ParameterValueForm(forms.ModelForm):

    class Meta:
        model = ParameterValue
        fields = "__all__"

    class Media:
        from django.conf import settings
        static_url = getattr(settings, 'STATIC_URL', '/static/')
        js = [ static_url+'admin/parameter_value_form.js', ]

    def __init__(self, *args, **kwargs):
        super(ParameterValueForm, self).__init__(*args, **kwargs)


class ParameterValueInline(admin.TabularInline):
    model = ParameterValue
    form = ParameterValueForm
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(ParameterValueInline, self).get_formset(request, obj, **kwargs)
        return formset

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(ParameterValueInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'parameter':
            if request._obj_ is not None:
                possible_parameters = map(lambda x: x.pk, request._obj_.asset_type.get_parameters()
                                          + request._obj_.asset_type.get_global_parameters()
                                          + request._obj_.asset_type.get_external_factors()
                                          + request._obj_.asset_type.get_aging_parameters())
                field.queryset = field.queryset.filter(pk__in=possible_parameters)
            else:
                field.queryset = field.queryset.none()

        return field


class AssetAdmin(admin.ModelAdmin):
    inlines = [
        ParameterValueInline,
    ]

    def __init__(self, *args, **kwargs):
        super(AssetAdmin, self).__init__(*args, **kwargs)
        self.change_form_template = "report.html"

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        form = super(AssetAdmin, self).get_form(request, obj, **kwargs)
        return form

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['parameters_values'] = json.dumps(Asset.objects.get(pk=object_id).get_paramaters_and_values())

        return super(AssetAdmin, self).change_view(request, object_id, form_url, extra_context=extra_context)


admin.site.register(Asset, AssetAdmin)

admin.site.register(ParameterValue,admin.ModelAdmin)