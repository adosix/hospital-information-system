from django import forms
from django.contrib.auth.models import User
from .models import Medical_problem
from users.models import AuthUser

class PatientMedicalProblemUpdateForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['username']
class DoctorMedicalProblemUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    class Meta:
        model = AuthUser
        fields = ['username']
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
