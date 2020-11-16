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
    id = models.IntegerField(primary_key=True, unique=True)
    Patient_ID =  models.IntegerField()
    Doctor_ID = models.IntegerField()
    Title = models.TextField()
    Description = models.TextField()
    Status = models.TextField()
    start_date =models.DateField()

    def get_absolute_url(self):
        return reverse('Medical_problem', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.id




class Doctor(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)

    def get_absolute_url(self):
        return reverse('doctor', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.id

class Patient(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)

    def get_absolute_url(self):
        return reverse('doctor', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.id
