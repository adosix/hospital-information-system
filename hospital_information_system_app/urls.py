from django.urls import path
from . import views

urlpatterns = [
    path(r'login/', views.loginPage, name ="login"),
    path(r'register/', views.registerPage, name ="register"),
    path(r'reservation/', views.reservation, name='reservation'),
    path(r'home/', views.homePage, name='home'),

    #$path('', views.user, name='hotel-home'),
    
]