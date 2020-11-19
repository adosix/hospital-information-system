from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect

import datetime
from django.utils import timezone

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
from .models import Medical_record
from users.models import AuthUser
from users.models import Profile
from .models import Doctor
from .models import Patient
from .models import Compensated_operations
from .models import Ticket
from .forms import MedicalProblemUpdateForm, MedicalProblemUsers, MedicalProblemCreate, CompensationOperationsCreate,UsersCompensation,Status,Record,TicketForm
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
def tickets_doc(request,pk):
    if request.method == 'POST':
        for name,value in request.POST.items():
            if value == "opened" or value == "closed":
                key = name
                status = value
        ticket = get_object_or_404(Ticket,id=key)
        medical_problem = get_object_or_404(Medical_problem, id = ticket.Medical_problem_ID)
        if(status == "opened"):
            tmp = False
            for r in Medical_record.objects.all():
                if ticket.id == r.Ticket_ID:
                    tmp = True
            if not tmp:
                messages.warning(request, f'Can not close ticket without record.')
                return HttpResponseRedirect("/tickets_doc/" + str(pk))
            ticket.Status = True
            ticket.save()
            medical_problem.Status = 0
            for t in Ticket.objects.all():
                if t.Medical_problem_ID == medical_problem.id and t.Status == False:
                    medical_problem.Status = 1
            medical_problem.save()
        else:
            ticket.Status = False
            ticket.save()
            medical_problem.Status = 1
            medical_problem.save()
    context = {
        'pk': pk,
        'Ticket': Ticket.objects.all(),
        'AuthUser': AuthUser.objects.all(),
        'Patient':  Patient.objects.all(),
        'Medical_problem':  Medical_problem.objects.all(),
    }

    return render(request, 'hospital_is/tickets_doc.html', context)
def tickets_admin(request):
    if request.method == 'POST':
        for name,value in request.POST.items():
            if value == "opened" or value == "closed":
                key = name
                status = value
        ticket = get_object_or_404(Ticket,id=key)
        medical_problem = get_object_or_404(Medical_problem, id = ticket.Medical_problem_ID)
        if(status == "opened"):
            tmp = False
            for r in Medical_record.objects.all():
                if ticket.id == r.Ticket_ID:
                    tmp = True
            if not tmp:
                messages.warning(request, f'Can not close ticket without record.')
                return HttpResponseRedirect("/tickets_admin/")
            ticket.Status = True
            ticket.save()
            medical_problem.Status = 0
            for t in Ticket.objects.all():
                if t.Medical_problem_ID == medical_problem.id and t.Status == False:
                    medical_problem.Status = 1
            medical_problem.save()
        else:
            ticket.Status = False
            ticket.save()
            medical_problem.Status = 1
            medical_problem.save()
    context = {
        'Ticket': Ticket.objects.all(),
        'AuthUser': AuthUser.objects.all(),
        'Patient':  Patient.objects.all(),
        'Medical_problem':  Medical_problem.objects.all(),
    }

    return render(request, 'hospital_is/tickets_admin.html', context)
def medical_problem_tickets(request, pk):
    if request.method == 'POST':

        for name,value in request.POST.items():
            if value == "opened" or value == "closed":
                key = name
                status = value
        try :
            ticket = get_object_or_404(Ticket, id = key)
        except:
            for name,value in request.POST.items():
                if value == "Delete":
                    key = name
            ticket = get_object_or_404(Ticket,id=key)
            medical_problem = get_object_or_404(Medical_problem, id = ticket.Medical_problem_ID)

            if ticket.Status == True:
                ticket.delete()
                medical_problem.Status = 0
                for t in Ticket.objects.all():
                    if t.Medical_problem_ID == medical_problem.id and t.Status == False:
                        medical_problem.Status = 1
                medical_problem.save()
                return HttpResponseRedirect("/medical_problem_tickets/" + str(pk))
            else:
                if request.user.is_superuser:
                    ticket.delete()
                    medical_problem.Status = 0
                    for t in Ticket.objects.all():
                        if t.Medical_problem_ID == medical_problem.id and t.Status == False:
                            medical_problem.Status = 1
                    medical_problem.save()
                    return HttpResponseRedirect("/medical_problem_tickets/" + str(pk))
                else :
                    messages.warning(request, f'Can not delete opened ticket.')
                    return HttpResponseRedirect("/medical_problem_tickets/" + str(pk))
        medical_problem = get_object_or_404(Medical_problem, id = ticket.Medical_problem_ID)


        if(status == "opened"):
            tmp = False
            for r in Medical_record.objects.all():
                if ticket.id == r.Ticket_ID:
                    tmp = True
            if not tmp:
                messages.warning(request, f'Can not close ticket without record.')
                return HttpResponseRedirect("/medical_problem_tickets/" + str(pk))
            ticket.Status = True
            ticket.save()
            medical_problem.Status = 0
            for t in Ticket.objects.all():
                if t.Medical_problem_ID == medical_problem.id and t.Status == False:
                    medical_problem.Status = 1
            medical_problem.updated=ticket.updated
            medical_problem.save()
        else:
            ticket.Status = False
            ticket.save()
            medical_problem.Status = 1
            medical_problem.updated=ticket.updated
            medical_problem.save()
    context = {
        'Medical_problem': Medical_problem.objects.all(),
        'Ticket' : Ticket.objects.all(),
        'pk':pk,
        'AuthUser': AuthUser.objects.all(),

        'doctor': Doctor.objects.all()
    }
    return render(request, 'hospital_is/medical_problem_tickets.html', context)
def medical_ticket_edit(request, pk):
    context = {
        'Medical_problem': Medical_problem.objects.all(),
        'Ticket' : Ticket.objects.all(),
        'pk':pk,
        'AuthUser': AuthUser.objects.all(),

        'doctor': Doctor.objects.all()
    }
    return render(request, 'hospital_is/medical_problem_tickets.html', context)
def medical_ticket_record(request, pk):
    try:
        record = get_object_or_404(Medical_record, Ticket_ID=pk)
        record_f = Record(instance=record)
    except:
        record_f = Record()
    if request.method == 'POST':
        try:
            record = get_object_or_404(Medical_record, Ticket_ID=pk)
            record_f = Record(request.POST,instance=record)
        except:
            record_f = Record(request.POST)
        ticket = get_object_or_404(Ticket, id=pk)
        if(request.user.id != ticket.Doctor_ID):
            messages.warning(request, f'You dont have permissions to update this file')
            return HttpResponseRedirect("/medical_ticket_record/" + str(pk))
        if(ticket.Status == True):
            messages.warning(request, f'Medical record can not be updated when the ticket is closed.')
            return HttpResponseRedirect("/medical_ticket_record/" + str(pk))
        if record_f.is_valid():
            record = record_f.save(commit=False)
            ticket=get_object_or_404(Ticket,id = pk)
            medical_problem=get_object_or_404(Medical_problem, id=ticket.Medical_problem_ID)
            ticket.updated = record.updated
            medical_problem.updated = record.updated
            ticket.save()
            medical_problem.save()
            record.Ticket_ID = ticket.id
            tmp = Medical_record.objects.all()
            try:
                tmp = tmp[len(tmp)-1]
                id = tmp.id+1
            except:
                id = 0
            record.id = id
            record.save()
            messages.success(request, f'Medical record updated.')
        else :
            messages.warning(request, f'Medical record not updated.')
    context = {
        'record_f':record_f,
        'Medical_problem': Medical_problem.objects.all(),
        'Ticket' : Ticket.objects.all(),
        'pk':pk,
        'AuthUser': AuthUser.objects.all(),

        'doctor': Doctor.objects.all()
    }
    return render(request, 'hospital_is/medical_ticket_record.html', context)

def medical_problem_edit(request, pk):
    status_f = Status()
    medical_problem = get_object_or_404(Medical_problem, id=pk)
    UserFormSet = modelformset_factory(AuthUser, form=MedicalProblemUsers,fields=('username',),min_num=2,max_num=2, validate_min=True, extra=2)
    patient = get_object_or_404(AuthUser, id = medical_problem.Patient_ID)
    doctor= get_object_or_404(AuthUser, id = medical_problem.Doctor_ID)
    if request.method == 'POST':
        status_f = request.POST['Status']
        formset = UserFormSet(request.POST or None, request.FILES or None)
        m_form = MedicalProblemUpdateForm(request.POST, instance=medical_problem)
        for form0 in formset:
            form0.save(commit=False)
        if m_form.is_valid() and formset.is_valid():
            if(status_f == '2'):
                for t in Ticket.objects.all():
                    if(t.Medical_problem_ID == pk and t.Status == False):
                        messages.warning(request, f'All tickets have to be done before closing medical problem.')
                        return HttpResponseRedirect("/medical_problem_edit/" + str(pk))
                medical_problem.Status = 2;
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






            timezone.deactivate()
            medical_problem.updated = datetime.datetime.now()

            if 'del' in request.POST:
                medical_problem.delete()
                messages.success(request, "Medical problem successfully deleted!")
                if request.user.is_superuser:
                    return HttpResponseRedirect("/medical_problems_admin/")
                else:
                    return HttpResponseRedirect("/medical_problems_doc/" + str(doctor.id))
            medical_problem.save()
            messages.success(request, f'Medical problem updated.')
            if request.user.is_superuser:
                return HttpResponseRedirect("/medical_problems_admin/")
            else:
                return HttpResponseRedirect("/medical_problems_doc/" + str(doctor.id))
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
        'Status' :status_f,
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
            if request.user.is_superuser:
                return HttpResponseRedirect("/medical_problems_admin/")
            else:
                return HttpResponseRedirect("/medical_problems_doc/" + str(doctor.id))
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
def medical_ticket_create(request,pk):

    t_form = TicketForm()
    user_f = UsersCompensation()
    if request.method == 'POST':
        medical_problem = get_object_or_404(Medical_problem, id=pk)
        if(medical_problem.Status == 2):
            messages.warning(request, f'Ticket   can not be updated when the med problem is finished.')
            return HttpResponseRedirect("/medical_problems_admin/" )
        t_form = TicketForm(request.POST)
        user_f = UsersCompensation(request.POST)
        if(t_form.is_valid() and user_f.is_valid()):
            user_f = user_f.save(commit=False)
            t_form = t_form.save(commit=False)
            user_f = get_object_or_404(AuthUser, username=user_f.username)
            t_form.Medical_problem_ID = pk
            t_form.Doctor_ID = user_f.id
            medical_problem.updated = t_form.updated
            medical_problem.Status = 1
            medical_problem.save()
            tmp = Ticket.objects.all()
            tmp = tmp[len(tmp)-1]
            t_form.id = tmp.id+1
            t_form.save()
            messages.success(request, f'Medical ticket created.')
            return HttpResponseRedirect("/medical_problem_tickets/" + str(pk))
        else:
            messages.warning(request, f'Medical ticket not created.')
            t_form = TicketForm()
            user_f = UsersCompensation()
    context = {
        'user_f': user_f,
        't_form': t_form,
        'Medical_problem': Medical_problem.objects.all(),
        'AuthUser': AuthUser.objects.all(),
        'Doctor': Doctor.objects.all(),
    }
    return render(request, 'hospital_is/medical_ticket_create.html', context)
def medical_problems_doc(request,pk):
    context = {
        'pk':pk,
        'AuthUser': AuthUser.objects.all(),
        'Medical_problem' : Medical_problem.objects.all(),
    }
    return render(request, 'hospital_is/medical_problems_doc.html',context)
def compensation_operations(request):
    context = {
        'Compensated_operations':  Compensated_operations.objects.all(),
    }
    return render(request, 'hospital_is/compensation_operations.html', context)
def compensation_operations_create(request):
    if request.method == 'POST':
        c_form = CompensationOperationsCreate(request.POST)
        p_form = UsersCompensation(request.POST)
        if c_form.is_valid() and p_form.is_valid():
            insurance_worker = p_form.save(commit=False)
            insurance_worker = get_object_or_404(AuthUser, username = insurance_worker.username)
            operation = c_form.save(commit=False)
            operation.creator = insurance_worker.id
            operation.save()
            messages.success(request, f'Compensation operation created.')
        elif c_form.is_valid() and request.user.is_superuser and request.user.is_staff==False:
            operation = c_form.save(commit=False)
            operation.creator = request.user.id
            operation.save()
            messages.success(request, f'Compensation operation created.')
        else:
            messages.warning(request, f'Compensation operation not created.')
    c_form = CompensationOperationsCreate()
    p_form = UsersCompensation()
    context = {
        'c_form': c_form,
        'p_form': p_form,
    }
    return render(request, 'hospital_is/compensation_operations_create.html', context)
def compensation_operations_edit(request,pk):
    compensated_operation = get_object_or_404(Compensated_operations, Operation=pk)
    if request.method == 'POST':
                c_form = CompensationOperationsCreate(request.POST,instance=compensated_operation)
                compensated_operation.delete()
                if c_form.is_valid():
                    c = c_form.save()
                    if 'del' in request.POST:
                        c.delete()
                        messages.success(request, "Compensation request successfully deleted!")
                        return HttpResponseRedirect("/compensation_operations/")
                    messages.success(request, f'Compensation operation updated.')
                    return HttpResponseRedirect("/compensation_operations_edit/"+c.Operation)

                else:
                    messages.warning(request, f'Compensation operation not updated.')
    c_form = CompensationOperationsCreate(instance=compensated_operation)
    context = {
        'pk' :pk,
        'c_form': c_form,
    }
    return render(request, 'hospital_is/compensation_operations_edit.html', context)
