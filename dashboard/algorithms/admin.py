from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from models.AssetType import Technology, AssetType, GlobalParameter
from models.Parameter import Parameter, ValueCorrespondence
from models.Component import Component
from models.Function import Function
from models.Fault import Fault


class TechnologyAdmin(admin.ModelAdmin):
    model = Technology
    save_as = True

admin.site.register(Technology, TechnologyAdmin)


class ValueCorrespondenceInline(NestedTabularInline):
    model = ValueCorrespondence
    fk_name = 'parameter'
    extra = 1
    save_as = True


class ParameterInline(NestedStackedInline):
    model = Parameter
    inlines = [ValueCorrespondenceInline]
    fk_name = 'fault'
    extra = 1
    save_as = True

#class FaultAdmin(NestedModelAdmin):
#    model = Fault
#    inlines = [ParameterInline]


#admin.site.register(Fault, FaultAdmin)

class FaultInline(NestedStackedInline):
    model = Fault
    inlines = [ParameterInline]
    fk_name = 'function'
    extra = 0
    save_as = True


class FunctionInline(NestedStackedInline):
    model = Function
    inlines = [FaultInline]
    fk_name = 'component'
    extra = 0
    save_as = True


class ComponentInline(NestedStackedInline):
    model = Component
    inlines = [FunctionInline]
    fk_name = 'asset'
    extra = 0
    save_as = True


class ParametersAdmin(admin.ModelAdmin):
    model = Parameter
    inlines = [ValueCorrespondenceInline]

    def queryset(self, request):
        return self.model.objects.all()


class GlobalParameterInline(admin.TabularInline):
    model = GlobalParameter
    extra = 0


class AssetTypeAdmin(NestedModelAdmin):
    model = AssetType
    inlines = [GlobalParameterInline, ComponentInline]
    save_as = True

admin.site.register(AssetType, AssetTypeAdmin)