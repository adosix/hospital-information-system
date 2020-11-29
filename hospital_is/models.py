from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from PIL import Image

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=datetime.now())
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
    image = models.ImageField(default='default.jpg',upload_to='medical_problems_media')
    Status = models.IntegerField(default=0)
    created =models.DateTimeField(default=datetime.now())
    updated =models.DateTimeField(default=datetime.now())

    def get_absolute_url(self):
        return reverse('Medical_problem', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    def get_pic(self):
        return "/media/"+str(self.image)
    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.id
class Medical_record(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    Ticket_ID =  models.IntegerField()
    Title = models.TextField()
    Description = models.TextField()
    created =models.DateTimeField(default=datetime.now())
    updated =models.DateTimeField(default=datetime.now())

    def get_absolute_url(self):
        return reverse('Medical_problem', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.id

class Picture(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    Image = models.ImageField(upload_to='medical_records_media')
    r_id =  models.IntegerField()
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.Image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.Image.path)
    def get_pic(self):
        return "/media/"+str(self.Image)
    def get_absolute_url(self):
        return reverse('Picture', kwargs={'pk': self.pk})
    class Meta:
        ordering = ['id']
    def __unicode__(self):
        return self.id
class Ticket(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    Medical_problem_ID =  models.IntegerField()
    Doctor_ID = models.IntegerField()
    Operation = models.TextField()
    Status = models.IntegerField(default=0)
    Description = models.TextField()
    created =models.DateTimeField(default=datetime.now())
    updated =models.DateTimeField(default=datetime.now())

    def get_absolute_url(self):
        return reverse('Medical_problem', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.id
class Compensation_request(models.Model):
    id=models.IntegerField(primary_key=True)
    ticket_id = models.IntegerField()
    Operation_r = models.TextField()
    Description_r = models.TextField()
    status = models.IntegerField(default=0)
    def get_absolute_url(self):
        return reverse('Compensation_request', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id']
    def __unicode__(self):
        return self.id
class Compensated_operations(models.Model):
    Operation = models.TextField(primary_key=True, unique=True)
    Description = models.TextField()
    Creator = models.IntegerField()


    def get_absolute_url(self):
        return reverse('Medical_problem', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['Operation']

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
    def delete(self,a=0):
        if a:
            raise RelatedRecordsExist("SomeModel has child records!")
class Patient(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)

    def get_absolute_url(self):
        return reverse('Patient', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.id
    def delete(self,a=0):
        if a:
            raise RelatedRecordsExist("SomeModel has child records!")
class Admin(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)

    def get_absolute_url(self):
        return reverse('admin', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.id
    def delete(self,a=0):
        if a:
            raise RelatedRecordsExist("SomeModel has child records!")
class Insurance_worker(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)

    def get_absolute_url(self):
        return reverse('insurance', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.id
    def delete(self,a=0):
        if a:
            raise RelatedRecordsExist("SomeModel has child records!")
