from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    medical_ticket_create,
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
     path('medical_ticket_record/<int:pk>/', views.medical_ticket_record, name='medical_ticket_record'),
     path('medical_problem_tickets/<int:pk>/', views.medical_problem_tickets, name='medical_problem_tickets'),
    #path('post/<int:pk>/',Medical_problem_DetailView.as_view(), name='post-detail'),
    path('medical_problem_create/', views.medical_problem_create, name='medical_problem_create'),
    path('medical_ticket_create/<int:pk>/', views.medical_ticket_create, name='medical_ticket_create'),
    path('users/', views.users, name='users'),
    path('medical_problems_admin/', views.medical_problems_admin, name='medical_problems_admin'),
    path('medical_problems_pac/<int:pk>/', views.medical_problems_pac, name='medical_problems_pac'),
    path('medical_problems_doc/<int:pk>/', views.medical_problems_doc, name='medical_problems_doc'),
    path('tickets_doc/<int:pk>/', views.tickets_doc, name='tickets_doc'),
    path('tickets_pac/<int:pk>/', views.tickets_pac, name='tickets_pac'),
    path('make_compensation/<int:pk>/', views.make_compensation, name='make_compensation'),
    path('compensation_request/', views.compensation_request, name='compensation_request'),
    path('compensation_operations/', views.compensation_operations, name='compensation_operations'),
    path('compensation_operations_create/', views.compensation_operations_create, name='compensation_operations_create'),
    path('compensation_operations_edit/<str:pk>/', views.compensation_operations_edit, name='compensation_operations_edit'),
    path('tickets_admin/', views.tickets_admin, name='tickets_admin'),
    path('contact/', views.contact, name='hospital_is-contact'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
