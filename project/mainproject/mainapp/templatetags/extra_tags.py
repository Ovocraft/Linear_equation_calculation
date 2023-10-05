from django import template

register = template.Library()

@register.filter(name='range')
def range_filter(value):
    return range(1, value+1)
