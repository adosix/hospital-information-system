from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse

class User(models.Model):
    id = models.SlugField(primary_key=True, unique=True, max_length=255)
    First_name  = models.TextField()
    Last_name   = models.TextField()
    Password    = models.TextField()
    Email       = models.TextField()
    TelNum      = models.TextField()
    State       = models.TextField()
    City        = models.TextField()
    Street      = models.TextField()

    def get_absolute_url(self):
        return reverse('user_details', args=[self.id])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super( User, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']

        def __unicode__(self):
            return self.id
"""
class Guests(models.Model):
    name = models.TextField()

    def get_absolute_url(self):
        return reverse('guest_details', args=[self.name])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']

        def __unicode__(self):
            return self.name
            """