__author__ = 'Afonso'
from django import template

register = template.Library()


@register.filter
def percentage(value):
    return "{}%".format(int(round(value, 0)))

@register.filter
def percentage_to_color(value):
    class_value = int(round(value/5.0, 0))
    if class_value < 1:
        class_value = 1
    elif class_value > 19:
        class_value = 19

    return class_value

@register.filter(name='list_iter')
def list_iter(lists):
    list_a, list_b, list_c = lists

    for x, y, z in zip(list_a, list_b, list_c):
        yield (x, y, z)

@register.filter(name='get_parameter_color')
def get_parameter_color(value):
    if value:
        if value.get_warning():
            return "rgb(254, 230, 42);"
        elif value.get_alert():
            return "#d9534F"

    return "inherit"