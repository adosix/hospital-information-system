from django import template
from users.models import AuthUser
register = template.Library()
import datetime

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

@register.filter(name='is_active')
def is_active(active):
    if active:
        return True
    return False

@register.filter(name='get_username')
def get_username(id, user):
    for u in user:
        if id == u.id:
            return u.username
@register.filter(name='get_username_ticket')
def get_username_ticket(id, med_p):
    for m in med_p:
        if id == m.id:
            return get_username(m.Patient_ID,AuthUser.objects.all())

@register.filter(name='get_first_name')
def get_first_name(id, user):
    for u in user:
        if id == u.id:
            return u.first_name

@register.filter(name='get_last_name')
def get_last_name(id, user):
    for u in user:
        if id == u.id:
            return u.last_name

@register.filter(name='return_date')
def return_date(date):
    return date.strftime('%Y-%m-%d')

