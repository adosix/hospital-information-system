from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    room_number = models.SlugField(unique=True, max_length=255)
    sleeps = models.TextField()
    price = models.TextField()
    wifi = models.TextField()
    tv = models.TextField()

    def get_absolute_url(self):
        return reverse('hotel_room_detail', args=[self.room_number])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['room_number']

        def __unicode__(self):
            return self.roomNumber

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