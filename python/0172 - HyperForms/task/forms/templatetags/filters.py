from django import template

register = template.Library()


@register.filter
def get(data, key):
    return data.get(key)
