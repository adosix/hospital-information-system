from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
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
from .forms import MedicalProblemUpdateForm, PatientMedicalProblemUpdateForm, DoctorMedicalProblemUpdateForm

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

def medical_problem_edit(request, pk):
    medical_problem = get_object_or_404(Medical_problem, id=pk)
    patient_i = get_object_or_404(AuthUser, id=medical_problem.Patient_ID)
    doctor_i = get_object_or_404(AuthUser, id=medical_problem.Doctor_ID)
    if request.method == 'POST':
        m_form = MedicalProblemUpdateForm(request.POST, instance=medical_problem)
        p_form = PatientMedicalProblemUpdateForm(request.POST,instance=patient_i)
        d_form = DoctorMedicalProblemUpdateForm(request.POST, instance=doctor_i)
        if m_form.is_valid()  and p_form.is_valid() and d_form.is_valid():
            messages.success(request, f'Medical problem updated.')
            msg = m_form.save(commit=False)
            pat = p_form.save(commit=False)

            doc = d_form.save(commit=False)
            doc = get_object_or_404(AuthUser, username=doc.username)
            pat = get_object_or_404(AuthUser, username=pat.username)
            msg.Patient_ID = 836
            msg.Doctor_ID = doc.id
            msg.save()
        else:
            messages.warning(request, f'Medical problem not updated.')
            medical_problem = get_object_or_404(Medical_problem, id=pk)
            patient_i = get_object_or_404(AuthUser, id=medical_problem.Patient_ID)
            doctor_i = get_object_or_404(AuthUser, id=medical_problem.Doctor_ID)
    m_form = MedicalProblemUpdateForm(instance=medical_problem)
    p_form = PatientMedicalProblemUpdateForm( instance=patient_i)
    d_form = DoctorMedicalProblemUpdateForm(instance=doctor_i)
    context = {
        'p_form' : p_form,
        'd_form' : d_form,
        'm_form' : m_form,


        'Medical_problem': Medical_problem.objects.all(),
        'AuthUser': AuthUser.objects.all(),
        'Doctor': Doctor.objects.all(),
    }

    return render(request, 'hospital_is/medical_problem_edit.html', context)

class Medical_problem_ListView(ListView):
    model = Medical_problem
    template_name = 'hospital_is/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'Medical_problem'
    ordering = ['-id']
    paginate_by = 20

class User_Medical_problem_ListView(ListView):
    model = Medical_problem
    template_name = 'hospital_is/user_posts.html'  # <app>/<model>_<viewtype>.html


    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class Medical_problem_DetailView(DetailView):
    model = Medical_problem

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
