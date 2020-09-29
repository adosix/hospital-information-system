from django.urls import path
from . import views

urlpatterns = [
    path('reservation/', views.about, name='hotel-reservation'),
    path('', views.home, name='hotel-home'),
    
]