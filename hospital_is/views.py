from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect

from django.db.models import Q
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from .models import Medical_problem
from users.models import AuthUser
from users.models import Profile
from .models import Doctor
from .models import Patient
from .forms import MedicalProblemUpdateForm, MedicalProblemUpdateUser,MedicalProblemCreate,MedicalProblemUsers
def default(request):
    context = {
        'Medical_problem': Medical_problem.objects.all(),
        'doctor': Doctor.objects.all()
    }
    return render(request, 'hospital_is/home.html', context)

def about(request):
    context = {
        'Medical_problem': Medical_problem.objects.all(),
        'doctor': Doctor.objects.all()
    }
    return render(request, 'hospital_is/about.html', context)

def users(request):
    context = {
        'AuthUser': AuthUser.objects.all(),
        'Profiles': Profile.objects.all()
    }
    return render(request, 'hospital_is/users.html', context)

def medical_problems_admin(request):
    context = {
        'Medical_problem': Medical_problem.objects.all(),
        'AuthUser': AuthUser.objects.all()
    }

    return render(request, 'hospital_is/medical_problems_admin.html', context)
def delete_medical_problem(request,pk):
    med_problem = get_object_or_404(Medical_problem, id=pk)
    if request.method == "POST" and request.user.is_authenticated and request.user.is_staff==True:
        med_problem.delete()
        messages.success(request, "Medical problem successfully deleted!")
        return HttpResponseRedirect("/profile/")
    context= {'med_problem': med_problem,              }

    return render(request, 'hospital_is/delete_medical_problem.html', context)
def medical_problem_edit(request, pk):
    medical_problem = get_object_or_404(Medical_problem, id=pk)
    UserFormSet = modelformset_factory(AuthUser, form=MedicalProblemUsers,fields=('username',),min_num=2,max_num=2, validate_min=True, extra=2)
    patient = get_object_or_404(AuthUser, id = medical_problem.Patient_ID)
    doctor= get_object_or_404(AuthUser, id = medical_problem.Doctor_ID)

    if request.method == 'POST':
        formset = UserFormSet(request.POST or None, request.FILES or None)
        m_form = MedicalProblemUpdateForm(request.POST, instance=medical_problem)
        for form0 in formset:
            form0.save(commit=False)
        if m_form.is_valid() and formset.is_valid():
            tmp = 0
            formset = formset.save(commit=False)
            if(len(formset) == 2):
                for form in formset:
                    if(tmp == 0):
                        patient = get_object_or_404(AuthUser, username=form.username)
                        patient_i = get_object_or_404(Patient, id=patient.id)

                        tmp = 1
                    else:
                        doctor = get_object_or_404(AuthUser, username=form.username)
                        doctor_i = get_object_or_404(Doctor, id = doctor.id)
            elif(len(formset) == 1):
                tmp = get_object_or_404(AuthUser, username=formset[0].username)
                print(tmp.username)
                if(Patient.objects.filter(id=tmp.id)):
                    patient = tmp
                else:
                    doctor = tmp
            medical_problem = m_form.save(commit=False)
            medical_problem.Patient_ID=patient.id
            medical_problem.Doctor_ID=doctor.id
            medical_problem.save()
            messages.success(request, f'Medical problem updated.')
        else:
            messages.warning(request, f'Medical problem not updated.')
            medical_problem = get_object_or_404(Medical_problem, id=pk)
            patient = get_object_or_404(AuthUser, id=medical_problem.Patient_ID)
            doctor = get_object_or_404(AuthUser, id=medical_problem.Doctor_ID)
        formset = UserFormSet(queryset=AuthUser.objects.all().order_by('is_staff').filter(Q(username=patient.username) | Q(username=doctor.username)))
    else:
        formset = UserFormSet(queryset=AuthUser.objects.all().order_by('is_staff').filter(Q(username=patient.username,is_staff=patient.is_staff) | Q(username=doctor.username,is_staff=doctor.is_staff)))
    m_form = MedicalProblemUpdateForm(instance=medical_problem)
    context = {
        'pk' : pk,
        'formset' : formset,
        'm_form' : m_form,
        'Medical_problem': Medical_problem.objects.all(),
        'AuthUser': AuthUser.objects.all(),
        'Doctor': Doctor.objects.all(),
    }

    return render(request, 'hospital_is/medical_problem_edit.html', context)

def medical_problem_create(request):
    UserFormSet = modelformset_factory(AuthUser, form=MedicalProblemUsers,fields=('username',),min_num=2,max_num=2, validate_min=True, extra=2)
    if request.method == 'POST':
        m_form = MedicalProblemCreate(request.POST)
        formset = UserFormSet(request.POST or None, request.FILES or None,queryset=AuthUser.objects.none())
        for form0 in formset:
            form0.save(commit=False)

        if m_form.is_valid() and formset.is_valid():
            tmp = 0
            formset = formset.save(commit=False)
            for form in formset:
                if(tmp == 0):
                    patient = get_object_or_404(AuthUser, username=form.username)
                    patient_i = get_object_or_404(Patient, id=patient.id)

                    tmp = 1
                else:
                    doctor = get_object_or_404(AuthUser, username=form.username)
                    doctor_i = get_object_or_404(Doctor, id = doctor.id)
            medical_problem = m_form.save(commit=False)
            tmp = Medical_problem.objects.all()
            tmp = tmp[len(tmp)-1]
            id = tmp.id + 1
            medical_problem.id = id
            medical_problem.Patient_ID=patient.id
            medical_problem.Doctor_ID=doctor.id
            medical_problem.save()
            messages.success(request, f'Medical problem created.')
        else:
            messages.warning(request, f'Medical problem not updated.')

        formset = UserFormSet(queryset=AuthUser.objects.none())
    else:

        formset = UserFormSet(queryset=AuthUser.objects.none())
    m_form = MedicalProblemCreate()
    context = {
        'm_form' :m_form,
        'formset' : formset,
    }
    return render(request, 'hospital_is/medical_problem_create.html', context)
def medical_problems_doc(request,pk):
    context = {
        'pk':pk,
        'AuthUser': AuthUser.objects.all(),
        'Medical_problem' : Medical_problem.objects.all(),
    }
    return render(request, 'hospital_is/medical_problems_doc.html',context)
class Medical_problem_ListView(ListView):
    model = Medical_problem
    template_name = 'hospital_is/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'Medical_problem'
    ordering = ['-id']
    paginate_by = 20
#netreba?
class User_Medical_problem_ListView(ListView):
    model = Medical_problem
    template_name = 'hospital_is/user_posts.html'  # <app>/<model>_<viewtype>.html


    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class Medical_problem_CreateView(LoginRequiredMixin, CreateView):
    model = Medical_problem
    fields = ['id','Patient_ID','Doctor_ID','Title', 'Description', 'Status']

    def form_valid(self, form):
        #form.instance.Doctor_ID = self.request.user
        return super().form_valid(form)

class Medical_problem_UpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Medical_problem
    fields = ['Title', 'Description', 'Status', 'Patient_ID']

    def form_valid(self, form):
        form.instance.Doctor_ID = self.request.user
        return super().form_valid(form)

    def test_func(self):
        Medical_problem = self.get_object()
        if self.request.user == Medical_problem.Doctor_ID:
            return True
        return False


class Medical_problem_DeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Medical_problem
    success_url = '/'

    def test_func(self):
        Medical_problem = self.get_object()
        if self.request.user == Medical_problem.Doctor_ID:
            return True
        return False
