__author__ = 'Afonso'
from django import template

register = template.Library()


@register.filter
def percentage(value):
    return "{}%".format(int(round(value,0)))