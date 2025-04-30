from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.filter
def not_in_list(field_name, exclude_list):
    return field_name not in exclude_list.split(',')
