from django import template
from django.contrib.staticfiles import finders

register = template.Library()


@register.filter
def static_file_exists(value):
    return finders.find(value) is not None


@register.simple_tag
def query_image_extension(value):
    white_list = {'.jpg', '.png', '.jpeg', '.gif', '.bmp', '.tiff', '.svg'}
    for file_extension in white_list:
        if finders.find(value + file_extension):
            return value + file_extension

    return value
