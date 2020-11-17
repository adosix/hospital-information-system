from django.urls import path
from .views import (
    delete_medical_problem,
    medical_problems_doc,
    medical_problem_create,
    medical_problem_edit,
    medical_problems_admin,
    Medical_problem_ListView,
    #Medical_problem_DetailView,
    #Medical_problem_CreateView,
    Medical_problem_UpdateView,
    Medical_problem_DeleteView,
    User_Medical_problem_ListView
)
from . import views

urlpatterns = [
    path('', views.default, name='hospital_is-home'),
    path('user/<str:username>', User_Medical_problem_ListView.as_view(), name='user-posts'),
     path('medical_problem_edit/<int:pk>/', views.medical_problem_edit, name='medical_problem_edit'),
    #path('post/<int:pk>/',Medical_problem_DetailView.as_view(), name='post-detail'),
    path('medical_problem_create/', views.medical_problem_create, name='medical_problem_create'),
    path('users/', views.users, name='users'),
    path('medical_problems_admin/', views.medical_problems_admin, name='medical_problems_admin'),
    path('medical_problems_doc/<int:pk>/', views.medical_problems_doc, name='medical_problems_doc'),
    path('medical_problem/<int:pk>/update/', Medical_problem_UpdateView.as_view(), name='update_medical_problem'),
    path('delete_medical_problem/<int:pk>/', views.delete_medical_problem, name='delete_medical_problem'),
    path('about/', views.about, name='hospital_is-about'),
]
