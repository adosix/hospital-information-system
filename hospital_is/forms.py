from django import forms
from django.contrib.auth.models import User
from .models import Medical_problem
from .models import Medical_record
from .models import Ticket,Picture
from .models import Compensated_operations
from .models import Compensation_request
from users.models import AuthUser
from django.db import models



class MedicalProblemUpdateForm(forms.ModelForm):
    Title = forms.CharField(max_length=150,
    widget=forms.TextInput(attrs={'style':'max-width: 24em'}),
    required=True)
    image = forms.ImageField(required=False)

    class Meta:
        model = Medical_problem
        fields = ['Title', 'Description','image']
class Status(forms.Form):

    Status = forms.TypedChoiceField(label = "Finished?",
        choices = ((0, "No"), (2, "Yes")),
        coerce = lambda x: bool(int(x)),
        widget = forms.RadioSelect,
        initial = '0',
        required = True,)
class MedicalProblemCreate(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Medical_problem
        fields = ['Title', 'Description', 'image']
class MedicalProblemUsers(forms.ModelForm):
    username = forms.CharField(required=True)

class UsersCompensation(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['username']
class ChooseOperation(forms.Form):
        def __init__(self,pk,initial,*args,**kwargs):
           super(ChooseOperation, self).__init__(*args, **kwargs)
           choices = []
           choices.append(['',''])
           for u  in Compensated_operations.objects.all():
               choices.append([u.Description,u.Operation])
           self.fields['Operation']=forms.ChoiceField(choices=choices, widget=forms.Select,required=False)
        Operation = forms.ChoiceField()
class MakeCompensation(forms.ModelForm):
    Operation_r = forms.CharField(required=False)
    Description_r = forms.CharField(required=False)

    class Meta:
        model = Compensation_request
        fields = ['Operation_r','Description_r' ]
class CompensationOperationsCreate(forms.ModelForm):
    class Meta:
        model = Compensated_operations
        fields = ['Operation', 'Description']
class Record(forms.ModelForm):

    class Meta:
        model = Medical_record
        fields = ['Title', 'Description']
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['Operation','Description']
class PictureForm(forms.ModelForm):
    Image = forms.ImageField(required=False)

    class Meta:
        model=Picture
        fields = ['Image']
