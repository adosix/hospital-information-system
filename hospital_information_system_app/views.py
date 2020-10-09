from django.shortcuts import render
from .models import User


def about (request):
    context = {
        'User': User.objects.all
    }
    return render(request, 'hospital_information_system/reservation.html', context)