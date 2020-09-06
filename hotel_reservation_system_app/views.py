from django.shortcuts import render

rooms = [
    {
        'roomnumber' : '1',
        'sleeps' : '3',
        'price' : '52'
    },
        {
        'roomnumber' : '2',
        'sleeps' : '1',
        'price' : '21'
    }
]

def home (request):
    return render(request, 'hotel_reservation_system/home.html')

def about (request):
    context = {
        'rooms': rooms
    }
    return render(request, 'hotel_reservation_system/reservation.html', context)