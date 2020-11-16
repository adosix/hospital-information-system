from django.urls import path
from .views import (
    medical_problem_edit,
    medical_problems_admin,
    Medical_problem_ListView,
    Medical_problem_DetailView,
    Medical_problem_CreateView,
    Medical_problem_UpdateView,
    Medical_problem_DeleteView,
    User_Medical_problem_ListView
)
from . import views

urlpatterns = [
    path('', views.default, name='hospital_is-home'),
    path('user/<str:username>', User_Medical_problem_ListView.as_view(), name='user-posts'),
     path('medical_problem_edit/<int:pk>/', views.medical_problem_edit, name='medical_problem_edit'),
    path('post/<int:pk>/',Medical_problem_DetailView.as_view(), name='post-detail'),
    path('post/new/', Medical_problem_CreateView.as_view(), name='post-create'),
    path('users/', views.users, name='users'),
    path('medical_problems_admin/', views.medical_problems_admin, name='medical_problems_admin'),
    path('post/<int:pk>/update/', Medical_problem_UpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', Medical_problem_DeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='hospital_is-about'),
]
