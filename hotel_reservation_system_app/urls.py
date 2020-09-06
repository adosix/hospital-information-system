from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='hotel-home'),
    path('reservation/', views.about, name='hotel-reservation'),
]