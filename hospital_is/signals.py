from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from .models import Profile

def pre_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, models.Model):
        instance.pre_delete_handler()
models.Model.signals.pre_delete.connect(pre_delete_handler)
