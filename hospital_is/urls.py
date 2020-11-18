from django.urls import path
from .views import (

    medical_problems_doc,
    medical_problem_create,
    medical_problem_edit,
    medical_problems_admin,
    compensation_operations,
    compensation_operations_create,
    compensation_operations_edit,
)
from . import views

urlpatterns = [
    path('', views.default, name='hospital_is-home'),
     path('medical_problem_edit/<int:pk>/', views.medical_problem_edit, name='medical_problem_edit'),
     path('medical_ticket_edit/<int:pk>/', views.medical_ticket_edit, name='medical_ticket_edit'),

     path('medical_problem_tickets/<int:pk>/', views.medical_problem_tickets, name='medical_problem_tickets'),
    #path('post/<int:pk>/',Medical_problem_DetailView.as_view(), name='post-detail'),
    path('medical_problem_create/', views.medical_problem_create, name='medical_problem_create'),
    path('users/', views.users, name='users'),
    path('medical_problems_admin/', views.medical_problems_admin, name='medical_problems_admin'),
    path('medical_problems_doc/<int:pk>/', views.medical_problems_doc, name='medical_problems_doc'),
    path('compensation_operations/', views.compensation_operations, name='compensation_operations'),
    path('compensation_operations_create/', views.compensation_operations_create, name='compensation_operations_create'),
    path('compensation_operations_edit/<str:pk>/', views.compensation_operations_edit, name='compensation_operations_edit'),
    path('tickets_admin/', views.tickets_admin, name='tickets_admin'),
    path('about/', views.about, name='hospital_is-about'),
]
