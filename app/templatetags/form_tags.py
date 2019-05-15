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
