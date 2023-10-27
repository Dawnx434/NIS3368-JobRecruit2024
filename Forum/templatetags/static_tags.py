from django import template
from django.contrib.staticfiles import finders

register = template.Library()


@register.filter
def static_file_exists(value):
    return finders.find(value) is not None
