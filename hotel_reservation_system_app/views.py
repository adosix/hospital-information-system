from django.shortcuts import render
from .models import Post

def home (request):
    return render(request, 'hotel_reservation_system/home.html')

def about (request):
    context = {
        'rooms': Post.objects.all()
    }
    return render(request, 'hotel_reservation_system/reservation.html', context)