from django.shortcuts import render
from .models import Post
from .models import Guests

def home (request):
    context = {
        'guests': Guests.objects.all
    }
    return render(request, 'hospital_information_system/home.html',context)

def about (request):
    context = {
        'rooms': Post.objects.all
    }
    return render(request, 'hospital_information_system/reservation.html', context)