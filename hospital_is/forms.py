from django import forms
from django.contrib.auth.models import User
from .models import Medical_problem
from .models import Compensated_operations
from users.models import AuthUser
from django.db import models



class MedicalProblemUpdateForm(forms.ModelForm):
    Title = forms.CharField(max_length=150,
    widget=forms.TextInput(attrs={'style':'max-width: 24em'}),
    required=True)
    Status = forms.CharField(max_length=150,
    widget=forms.TextInput(attrs={'style':'max-width: 24em'}),
    required=True)
    class Meta:
        model = Medical_problem
        fields = ['Title', 'Description','Status']

class MedicalProblemCreate(forms.ModelForm):

    class Meta:
        model = Medical_problem
        fields = ['Title', 'Description','Status','start_date']
class MedicalProblemUsers(forms.ModelForm):
    username = forms.CharField(required=True)
class UsersCompensation(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['username']
class CompensationOperationsCreate(forms.ModelForm):
    class Meta:
        model = Compensated_operations
        fields = ['Operation', 'Description']
