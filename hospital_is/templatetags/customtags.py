from django import template

register = template.Library()

# 1 1 admin
# 1 0 insurance worker
# 0 1 doctor
# 0 0 patient

@register.filter(name='is_insurance_w')
def is_insurance_w(user):
    if not user.is_staff and user.is_superuser:
        return True
    return False

@register.filter(name='is_doctor')
def is_doctor(user):
    if user.is_staff and not user.is_superuser :
        return True
    return False

@register.filter(name='is_admin')
def is_admin(user):
    if user.is_staff and user.is_superuser:
        return True
    return False

@register.filter(name='is_user')
def is_user(user):
    if not user.is_staff and not user.is_superuser:
        return True
    return False