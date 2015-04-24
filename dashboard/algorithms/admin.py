from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedTabularInline, NestedModelAdmin
from models.AssetType import Technology, AssetType
from models.Parameter import Parameter, ValueCorrespondence
from models.Component import Component
from models.Function import Function
from models.Fault import Fault

admin.site.register(Technology)


class ValueCorrespondenceInline(NestedTabularInline):
    model = ValueCorrespondence
    fk_name = 'parameter'
    extra = 3


class ParameterInline(NestedStackedInline):
    model = Parameter
    inlines = [ValueCorrespondenceInline]
    fk_name = 'fault'
    extra = 1


#class FaultAdmin(NestedModelAdmin):
#    model = Fault
#    inlines = [ParameterInline]


#admin.site.register(Fault, FaultAdmin)

class FaultInline(NestedStackedInline):
    model = Fault
    inlines = [ParameterInline]
    fk_name = 'function'
    extra = 1


class FunctionInline(NestedStackedInline):
    model = Function
    inlines = [FaultInline]
    fk_name = 'component'
    extra = 1


class ComponentInline(NestedStackedInline):
    model = Component
    inlines = [FunctionInline]
    fk_name = 'asset'
    extra = 2


class AssetTypeAdmin(NestedModelAdmin):
    model = AssetType
    inlines = [ComponentInline]

admin.site.register(AssetType, AssetTypeAdmin)