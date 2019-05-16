import re

from django import template

register = template.Library()


@register.filter
def tabindex(value, index):
    value.field.widget.attrs['tabindex'] = index
    return value


@register.filter
def disable_field(field, editable):
    if not editable:
        field.field.widget.attrs['disabled'] = 'disabled'
    return field


@register.simple_tag(takes_context=True)
def divide(context, num1, num2):
    from decimal import Decimal
    if not isinstance(num1, (int, Decimal, float)):
        num1 = getattr(context, num1, 0)

    try:
        num1 = Decimal(num1)
    except Exception:
        num1 = Decimal(0)

    if not isinstance(num1, (int, Decimal, float)):
        num2 = getattr(context, num2, 0)

    try:
        num2 = Decimal(num2)
    except Exception:
        num2 = Decimal(0)

    return (num1 / num2) if num2 > 0 else 0
