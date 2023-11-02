from django import template
from aintdoinit.constants import COLOR_CSS_MAP

register = template.Library()

@register.filter
def color_code(value):
    print("Color Value: ", value)
    return COLOR_CSS_MAP.get(value, 'transparent')