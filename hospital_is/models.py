from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Medical_problem(models.Model):
    id = models.SlugField(primary_key=True, unique=True, max_length=255)
    Patient_ID = models.TextField()
    Doctor_ID = models.TextField()
    Title = models.TextField()
    Description = models.TextField()
    Status = models.TextField()
    
    def get_absolute_url(self):
        return reverse('Medical_problem', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.id

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.BooleanField()
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'
        ordering = ['id']



class Doctor(models.Model):
    id = models.SlugField(primary_key=True, unique=True, max_length=255)
    
    def get_absolute_url(self):
        return reverse('doctor', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.id

class Patient(models.Model):
    id = models.SlugField(primary_key=True, unique=True, max_length=255)
    
    def get_absolute_url(self):
        return reverse('doctor', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.id

