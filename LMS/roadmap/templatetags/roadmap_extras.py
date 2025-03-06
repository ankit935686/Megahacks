from django import template
import re

register = template.Library()

@register.filter
def split(value, arg):
    return value.split(arg)

@register.filter
def startswith(value, arg):
    return value.startswith(arg)

@register.filter
def strip(value):
    return value.strip() 