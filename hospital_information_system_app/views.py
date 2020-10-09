from django.shortcuts import render, redirect
from .models import User
from .forms import RegisterForm
from .authentication import authenticate


def reservation (request):
    context = {
        'User': User.objects.all
    }
    return render(request, 'hospital_information_system/reservation.html', context)

def loginPage(request):
    context = {}
    return render(request, 'hospital_information_system/login.html')


def homePage(request):
    context = {}
    return render(request, 'hospital_information_system/home.html')



def registerPage(request):
    form = RegisterForm()

    context = {
        'form':form
    }
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            access = authenticate(username=username, password=password)
            if access is not None:
                if access: #access.is_active:
                    #login(request,access)
                    return render(request,'hospital_information_system/home.html')
                else:
                    return render(request, 'hospital_information_system/home.html')
        else:
            render(request,'hospital_information_system/home.html')
    else:
        return render(request, 'hospital_information_system/register.html',context)
    

