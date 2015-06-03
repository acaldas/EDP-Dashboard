from django import forms
from django.contrib import admin
from grappelli_nested.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from grappelli_nested.forms import BaseNestedModelForm
#from nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from models.AssetType import Technology, AssetType, GlobalParameter
from models.Parameter import Parameter, ValueCorrespondence, Parameters
from models.Component import Component
from models.Function import Function
from models.Fault import Fault, ExternalFactor, Faults


class FaultsForm(BaseNestedModelForm):
    class Meta:
        model = Faults
        fields = "__all__"

    parameters = forms.ModelMultipleChoiceField(label="Parameters", queryset=Parameter.objects.all())

    def __init__(self, *args, **kwargs):
        super(FaultsForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['parameters'].initial = self.instance.parameter_set.all()

    def save(self, *args, **kwargs):
        # FIXME: 'commit' argument is not handled
        # TODO: Wrap reassignments into transaction
        # NOTE: Previously assigned Foos are silently reset
        instance = super(FaultsForm, self).save(commit=False)
        self.fields['parameters'].initial.update(fault=None)
        self.cleaned_data['parameters'].update(fault=instance)
        return instance


class ValueCorrespondenceInline(NestedTabularInline):
    model = ValueCorrespondence
    fk_name = 'parameter'
    extra = 1
    save_as = True

    def queryset(self, request):
        return self.model.objects.all()


class ParameterInline(NestedStackedInline):
    model = Parameter
    inlines = [ValueCorrespondenceInline, ]
    fk_name = 'fault'
    extra = 1
    save_as = True

    def queryset(self, request):
        return self.model.objects.all()


class AgingParameterInline(NestedStackedInline):
    model = Parameter
    inlines = [ValueCorrespondenceInline, ]
    extra = 1
    save_as = True

    def queryset(self, request):
        return self.model.objects.all()


class TechnologyAdmin(NestedModelAdmin):
    model = Technology
    inlines = [AgingParameterInline, ]
    save_as = True

    def queryset(self, request):
        return self.model.objects.all()

admin.site.register(Technology, TechnologyAdmin)


class FaultInline(NestedStackedInline):
    model = Fault
    inlines = [ParameterInline, ]
    #form = FaultsForm
    fk_name = 'function'
    extra = 1
    save_as = True

    def queryset(self, request):
        return self.model.objects.all()


class FunctionInline(NestedStackedInline):
    model = Function
    inlines = [FaultInline,]
    fk_name = 'component'
    extra = 1
    save_as = True

    def queryset(self, request):
        return self.model.objects.all()


class ComponentInline(NestedStackedInline):
    model = Component
    inlines = [FunctionInline, ]
    fk_name = 'asset'
    extra = 0
    save_as = True

    def queryset(self, request):
        return self.model.objects.all()


class ParametersAdmin(admin.ModelAdmin):
    model = Parameters
    inlines = [ValueCorrespondenceInline, ]
    save_as = True

    def queryset(self, request):
        return self.model.objects.all()
admin.site.register(Parameters, ParametersAdmin)


class GlobalParameterInline(NestedTabularInline):
    model = GlobalParameter
    fk_name = 'asset'
    extra = 0
    inlines = []

    def queryset(self, request):
        return self.model.objects.all()


class AssetTypeAdmin(NestedModelAdmin):
    model = AssetType
    inlines = [GlobalParameterInline, ComponentInline, ]
    save_as = True
    list_display = ('name', 'technology')

admin.site.register(AssetType, AssetTypeAdmin)


class ExternalFactorInline(admin.TabularInline):
    model = ExternalFactor
    extra = 0
    save_as = True
    inlines = []

    def queryset(self, request):
        return self.model.objects.all()


class FaultsAdmin(admin.ModelAdmin):
    model = Faults
    #form = FaultsForm
    inlines = [ExternalFactorInline,]
    list_display = ('name', 'get_asset')

    def get_asset(self, obj):
        return obj.function.component.asset

    get_asset.short_description = 'Ativo'
    get_asset.admin_order_field = 'function__component__asset'

    def queryset(self, request):
        return self.model.objects.all()

admin.site.register(Faults, FaultsAdmin)