from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import Profile
from .models import AuthUser
from django.forms import HiddenInput
import datetime


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email', 'password1', 'password2']

class ProfileRegisterForm(forms.ModelForm):
    birth_date = forms.DateField(required=True)
    class Meta:
        model = Profile
        fields = ['image','birth_date']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(),
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = AuthUser
        fields = ['username', 'email','first_name', 'last_name', 'password']
class AdminUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(),
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = AuthUser
        fields = ['username', 'email','first_name', 'last_name', 'is_active', 'password']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','birth_date']
class UserRoleForm(forms.Form):

    Role = forms.TypedChoiceField(label = "Choose role",
        choices = ((1, "Pacient"), (0, "Admin"),(2,"Insurance_worker"),(3,"Doctor")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,)
