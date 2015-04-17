__author__ = 'Afonso'

from django.contrib import admin
from models import RegressionFunction, FunctionValue


class FunctionValueInline(admin.TabularInline):
    model = FunctionValue


class RegressionFunctionAdmin(admin.ModelAdmin):
    inlines = (
        FunctionValueInline,
    )

admin.site.register(RegressionFunction, RegressionFunctionAdmin)