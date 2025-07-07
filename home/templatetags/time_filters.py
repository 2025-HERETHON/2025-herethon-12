from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def time_since_custom(value):
    now = timezone.now()
    diff = now - value

    minutes = int(diff.total_seconds() // 60)
    hours = minutes // 60
    days = diff.days
    months = days // 30
    years = days // 365

    if minutes < 1:
        return "방금 전"
    elif minutes < 60:
        return f"{minutes}분 전"
    elif hours < 24:
        return f"{hours}시간 전"
    elif days < 30:
        return f"{days}일 전"
    elif days < 365:
        return f"{months}달 전"
    else:
        return f"{years}년 전"
