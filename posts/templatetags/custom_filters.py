# your_app/templatetags/custom_filters.py
from django import template
register = template.Library()

@register.filter
def index(sequence, position):
    try:
        return sequence[int(position)]
    except Exception as e:
        print(f"[index error] {e}")
        return ''
