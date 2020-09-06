from django.shortcuts import render
from .models import Post

rooms = [
    {
        'roomNumber' : '1',
        'sleeps' : '3',
        'price' : '52'
    },
        {
        'roomNumber' : '2',
        'sleeps' : '1',
        'price' : '21'
    }
]

def home (request):
    return render(request, 'hotel_reservation_system/home.html')

def about (request):
    context = {
        'rooms': Post.objects.all()
    }
    return render(request, 'hotel_reservation_system/reservation.html', context)