from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import Profile
from .models import AuthUser
from django.forms import HiddenInput
import datetime


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    first_name = forms.CharField(required=True,max_length=150)
    last_name = forms.CharField(required=True,max_length=150)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'password1', 'password2']
class DateInput(forms.DateInput):
    input_type= 'date'
class ProfileRegisterForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = Profile
        widgets= {'birth_date' : DateInput()
        }
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

class ChooseDoctor(forms.Form):

     def __init__(self,pk,initial,*args,**kwargs):
        super(ChooseDoctor, self).__init__(*args, **kwargs)
        choices = []
        for u  in AuthUser.objects.all():
            if u.is_staff and not u.is_superuser and not u.id==pk :
                choices.append([u.username,u.username])
        self.fields['Doctor']=forms.ChoiceField(choices=choices, widget=forms.Select)
        self.fields['Doctor'].initial = initial
     Doctor = forms.ChoiceField()
class ChoosePatient(forms.Form):

     def __init__(self,pk,initial,*args,**kwargs):
        super(ChoosePatient, self).__init__(*args, **kwargs)
        choices = []
        for u  in AuthUser.objects.all():
            if not u.is_staff and not u.is_superuser and not u.id==pk :
                choices.append([u.username,u.username])
        self.fields['Patient']=forms.ChoiceField(choices=choices, widget=forms.Select)
        self.fields['Patient'].initial = initial
     Patient = forms.ChoiceField()
class ChooseInsurance_worker(forms.Form):

     def __init__(self,pk,initial,*args,**kwargs):
        super(ChooseInsurance_worker, self).__init__(*args, **kwargs)
        choices = []
        for u  in AuthUser.objects.all():
            if not u.is_staff and u.is_superuser and not u.id==pk :
                choices.append([u.username,u.username])
        self.fields['Insurance']=forms.ChoiceField(choices=choices, widget=forms.Select)
        self.fields['Insurance'].initial = initial
     Insurance = forms.ChoiceField()
class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = Profile
        widgets= {'birth_date' : DateInput()}
        fields = ['image','birth_date']
class UserRoleForm(forms.Form):

    Role = forms.TypedChoiceField(label = "Choose role",
        choices = ((1, "Patient"), (0, "Admin"),(2,"Insurance_worker"),(3,"Doctor")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '1',
        required = True,)
