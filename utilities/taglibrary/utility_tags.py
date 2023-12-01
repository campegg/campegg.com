from django import template
from django.conf import settings
from django.utils.html import mark_safe
import math


register = template.Library()


@register.filter("readtime")
def readtime(source):
    try:
        return math.ceil(int(source) / 200)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter("placeholder")
def placeholder(value, text):
    if not hasattr(value, "field"):
        print(f"Debug: Wrong type passed to placeholder filter: {type(value)}")
        return value
    value.field.widget.attrs["placeholder"] = text
    return value


@register.simple_tag
def inline_svg(filename):
    # try STATICFILES_DIRS first
    for staticfiles_dir in settings.STATICFILES_DIRS:
        file_path = staticfiles_dir / filename
        if file_path.exists():
            with open(file_path, "r") as f:
                svg = f.read()
            return mark_safe(svg)

    # if not found, try STATIC_ROOT
    file_path = settings.STATIC_ROOT / filename
    if file_path.exists():
        with open(file_path, "r") as f:
            svg = f.read()
        return mark_safe(svg)

    # If still not found, return an empty string or some default value
    return mark_safe("<span class='error'>No SVG found!</span>")
