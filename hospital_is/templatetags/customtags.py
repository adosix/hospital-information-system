from django import template

register = template.Library()


@register.filter(name='id_eq')
def ifinlist(value, list):
    for v in list:
        if value == v.id :
            return True
    return False