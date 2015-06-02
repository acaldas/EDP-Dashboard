__author__ = 'Afonso'

from django.contrib import admin
from models import RegressionFunction, FunctionValue


class FunctionValueInline(admin.TabularInline):
    model = FunctionValue
    save_as=True

class RegressionFunctionAdmin(admin.ModelAdmin):
    inlines = (
        FunctionValueInline,
    )
    save_as = True

admin.site.register(RegressionFunction, RegressionFunctionAdmin)