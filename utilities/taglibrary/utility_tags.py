from django import template
from django.conf import settings
from django.utils.html import mark_safe
import math
import re


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


@register.filter("lnglat")
def lnglat(latlng):
    latlng = str(latlng).replace("[", "").replace("]", "")
    lat = latlng.split(", ")[0]
    lng = latlng.split(", ")[1]
    lnglat = "[" + lng + ", " + lat + "]"
    return mark_safe(lnglat)


@register.filter("lat")
def lat(latlng):
    if latlng:
        latlng = str(latlng).replace("[", "").replace("]", "")
        lat = latlng.split(", ")[0]
    else:
        lat = None
    return mark_safe(lat)


@register.filter("lng")
def lng(latlng):
    if latlng:
        latlng = str(latlng).replace("[", "").replace("]", "")
        lng = latlng.split(", ")[1]
    else:
        lng = None
    return mark_safe(lng)


@register.filter("m_to_km")
def convert_m_to_km(m):
    return round(m * 0.001, 2)


@register.filter("m_to_mi")
def convert_m_to_mi(m):
    return round(m * 0.0006213712, 2)


@register.filter("m_to_ft")
def convert_m_to_ft(m):
    return round(m * 3.28084, 2)


@register.filter("ms_to_minkm")
def convert_ms_to_minkm(ms):
    secs = round(60 / (ms / 16.666666666667 * 60), 10) * 60
    minutes, seconds = divmod(secs, 60)
    pace = "{:01}:{:02}".format(int(minutes), int(seconds))
    return pace


@register.filter("ms_to_minmi")
def convert_ms_to_minmi(ms):
    secs = round(60 / (ms / 26.8224 * 60), 10) * 60
    minutes, seconds = divmod(secs, 60)
    pace = "{:01}:{:02}".format(int(minutes), int(seconds))
    return pace


@register.filter("ms_to_kph")
def convert_ms_to_kph(ms):
    return round(ms * 3.6, 2)


@register.filter("ms_to_mph")
def convert_ms_to_mph(ms):
    return round(ms * 2.2369, 2)


@register.filter("kph_to_mph")
def convert_kph_to_mph(ms):
    return round(ms / 1.609344, 2)


@register.filter("c_to_f")
def convert_c_to_f(temp):
    return temp * 9 / 5 + 32


@register.filter("activitytime")
def display_activity_time(time):
    minutes, seconds = divmod(time, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    if hours == 0:
        act_time = "{:01}:{:02}".format(int(minutes), int(seconds))
    elif days == 0:
        act_time = "{:01}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    else:
        act_time = "{:01}:{:02}:{:02}:{:02}".format(
            int(days), int(hours), int(minutes), int(seconds)
        )
    return act_time


@register.filter("percent")
def display_percentage(value):
    return value * 100


@register.filter("sentencecase")
def sentencecase(string):
    return str(string).capitalize()


@register.filter("winddir")
def display_wind_direction(bearing):
    bearing_convert = round(bearing / 22.5, 0)
    if bearing_convert == 0:
        dir = "North"
    elif bearing_convert == 1:
        dir = "North-Northeast"
    elif bearing_convert == 2:
        dir = "Northeast"
    elif bearing_convert == 3:
        dir = "East-Northeast"
    elif bearing_convert == 4:
        dir = "East"
    elif bearing_convert == 5:
        dir = "East-Southeast"
    elif bearing_convert == 6:
        dir = "Southeast"
    elif bearing_convert == 7:
        dir = "South-Southeast"
    elif bearing_convert == 8:
        dir = "South"
    elif bearing_convert == 9:
        dir = "South-Southwest"
    elif bearing_convert == 10:
        dir = "Southwest"
    elif bearing_convert == 11:
        dir = "West-Southwest"
    elif bearing_convert == 12:
        dir = "West"
    elif bearing_convert == 13:
        dir = "West-Northwest"
    elif bearing_convert == 14:
        dir = "Northwest"
    elif bearing_convert == 15:
        dir = "North-Northwest"
    elif bearing_convert == 16:
        dir = "North"
    return dir


@register.filter
def account_name(url):
    pattern = r"https?://[^/]+/@([^/@]+)"
    match = re.search(pattern, url)
    if match:
        return f"@{match.group(1)}"
    return url


@register.filter
def account_url(url):
    pattern = r"https?://(?:[^/]+/)?@([^/@]+)(?:@([^/]+))?"
    match = re.search(pattern, url)
    if match:
        account, domain_b = match.groups()
        domain = domain_b if domain_b else url.split("/")[2]
        return f"https://{domain}/@{account}"
    return url


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
