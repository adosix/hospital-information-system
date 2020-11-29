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
from users.forms import ChooseDoctor
from users.forms import ChoosePacient
from users.forms import ChooseInsurance_worker
from .models import Doctor
from .models import Admin
from .models import Patient
from .models import Compensated_operations
from .models import Compensation_request
from .models import Ticket,Picture
from .forms import MedicalProblemUpdateForm, BaseMyFormSet,MedicalProblemUsers, MedicalProblemCreate, CompensationOperationsCreate,UsersCompensation,Status,Record,TicketForm,MakeCompensation,ChooseOperation,PictureForm
from django.forms import modelformset_factory

def default(request):
    context = {
        'Medical_problem': Medical_problem.objects.all(),
        'doctor': Doctor.objects.all()
    }
    return render(request, 'hospital_is/home.html', context)

def contact(request):
    context = {
        'Medical_problem': Medical_problem.objects.all(),
        'doctor': Doctor.objects.all()
    }
    return render(request, 'hospital_is/contact.html', context)

def users(request):
    context = {
        'AuthUser': AuthUser.objects.all(),
        'Profiles': Profile.objects.all()
    }
    return render(request, 'hospital_is/users.html', context)
def compensation_request(request):

    if request.method == 'POST':
        for name,value in request.POST.items():
            if value == "Decline" or value == "Accept" or value == 'Pending':
                key = name
                status = value
        request=get_object_or_404(Compensation_request,id=key)
        if(value=='Decline'):
            request.status=2
        elif(value=='Accept'):
            request.status=1
        else:
            request.status=0
        request.save()
        return HttpResponseRedirect("/compensation_request/")

    context = {
            'Ticket': Ticket.objects.all(),
        'AuthUser': AuthUser.objects.all(),
        'Compensation_request': Compensation_request.objects.all(),
    }
    return render(request, 'hospital_is/compensation_request.html', context)
def make_compensation(request, pk):
    m_form = MakeCompensation()
    c_form = ChooseOperation(-1,'')
    if request.method == 'POST':
        m_form = MakeCompensation(request.POST)
        c_r= request.POST['Operation']

        if m_form.is_valid():
            tmp = Compensation_request.objects.all()
            try:
                tmp = tmp[len(tmp)-1]
                id = tmp.id+1
            except:
                id = 0
            try:
                c = get_object_or_404(Compensated_operations, Description=c_r)
                tmp= Compensation_request.objects.create(id=id,ticket_id = pk,Operation_r=c.Operation,Description_r=c.Description)
            except:

                c = m_form.save(commit=False)
                c.ticket_id=pk
                c.id=id
                c.save()

            messages.success(request, f'Request made updated.')
            if request.user.is_superuser:
                return HttpResponseRedirect("/tickets_admin/" )
            else :
                return HttpResponseRedirect("/tickets_doc/"+str(request.user.id) )
    context = {
    'c_form':c_form,
    'm_form':m_form,
    'C_ope': Compensated_operations.objects.all(),
        'AuthUser': AuthUser.objects.all(),
        'Profiles': Profile.objects.all()
    }
    return render(request, 'hospital_is/make_compensation.html', context)

def medical_problems_admin(request):
    context = {
        'Medical_problem': Medical_problem.objects.all(),
        'AuthUser': AuthUser.objects.all()
    }
    return render(request, 'hospital_is/medical_problems_admin.html', context)

def medical_problems_pac(request,pk):
    context = {
        'pk':pk,
        'AuthUser': AuthUser.objects.all(),
        'Medical_problem' : Medical_problem.objects.all(),
    }
    return render(request, 'hospital_is/medical_problems_pac.html',context)

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
            ticket.Status = 1
            ticket.save()
            medical_problem.Status = 0
            for t in Ticket.objects.all():
                if t.Medical_problem_ID == medical_problem.id and t.Status == 0:
                    medical_problem.Status = 1
            medical_problem.save()
        else:
            ticket.Status = 0
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

def tickets_pac(request,pk):

    context = {
        'pk': pk,
        'Ticket': Ticket.objects.all(),
        'AuthUser': AuthUser.objects.all(),
        'Patient':  Patient.objects.all(),
        'Medical_problem':  Medical_problem.objects.all(),
    }
    return render(request, 'hospital_is/tickets_pac.html', context)
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
            ticket.Status = 1
            ticket.save()
            medical_problem.Status = 0
            for t in Ticket.objects.all():
                if t.Medical_problem_ID == medical_problem.id and t.Status == 0:
                    medical_problem.Status = 1
            medical_problem.save()
        else:
            ticket.Status = 0
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
            if value == "opened" or value == "closed" :
                key = name
                status = value
        try :
            ticket = get_object_or_404(Ticket, id = key)
        except:
            key = 0
            for name,value in request.POST.items():
                try:
                    if int(value) >= 0 :
                        key = name
                except Exception as e:
                    key = name

            ticket = get_object_or_404(Ticket,id=key)
            medical_problem = get_object_or_404(Medical_problem, id = ticket.Medical_problem_ID)

            if ticket.Status == 0 or ticket.Status==2:
                ticket.delete()
                medical_problem.Status = 0
                for t in Ticket.objects.all():
                    if t.Medical_problem_ID == medical_problem.id and t.Status ==0:
                        medical_problem.Status = 1
                medical_problem.save()
                return HttpResponseRedirect("/medical_problem_tickets/" + str(pk))
            else:
                if request.user.is_superuser:
                    ticket.delete()
                    medical_problem.Status = 0
                    for t in Ticket.objects.all():
                        if t.Medical_problem_ID == medical_problem.id and t.Status == 0:
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
            ticket.Status = 1
            ticket.save()
            medical_problem.Status = 0
            for t in Ticket.objects.all():
                if t.Medical_problem_ID == medical_problem.id and t.Status == 0:
                    medical_problem.Status = 1
            medical_problem.updated=ticket.updated
            medical_problem.save()
        else:
            ticket.Status = 0
            ticket.save()
            medical_problem.Status = 1
            medical_problem.updated=ticket.updated
            medical_problem.save()
    context = {
        'Medical_problem': Medical_problem.objects.all(),
        'm_problem': get_object_or_404(Medical_problem, id =pk),
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
        'Record': Medical_record.objects.all(),
        'doctor': Doctor.objects.all()
    }
    return render(request, 'hospital_is/medical_problem_tickets.html', context)
def medical_ticket_record(request, pk):
    try:
        record = get_object_or_404(Medical_record, Ticket_ID=pk)
        record_f = Record(instance=record)
        PictureFormSet = modelformset_factory(Picture,form=PictureForm,fields=('Image',))
        initial=[{'Image': x.Image,'id': x.id}  for x in Picture.objects.all() if x.r_id == record.id ]
        formset=PictureFormSet(queryset=Picture.objects.none(),initial=initial)
        formset.extra = len(initial)+1

    except:

        record_f = Record()
        PictureFormSet = modelformset_factory(Picture,form=PictureForm,fields=('Image',))
        formset=PictureFormSet(queryset=Picture.objects.none())
    if request.method == 'POST':
        try:
            record = get_object_or_404(Medical_record, Ticket_ID=pk)
            record_f = Record(request.POST,instance=record)
        except:
            record_f = Record(request.POST,request.FILES)
        formset=PictureFormSet(request.POST,request.FILES)
        ticket = get_object_or_404(Ticket, id=pk)
        if(request.user.id != ticket.Doctor_ID and(not request.user.is_superuser and not request.user.is_staff)):
            messages.warning(request, f'You dont have permissions to update this file')
            return HttpResponseRedirect("/medical_ticket_record/" + str(pk))
        if(ticket.Status == 1):
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
            try:
                id = record.id
                r=record.save()

            except:

                tmp = Medical_record.objects.all()
                try:
                    tmp = tmp[len(tmp)-1]
                    id = tmp.id+1
                except:
                    id = 0
                record.id = id
                r=record.save()
            instance =formset.save(commit=False)

            initial=[{'Image': x.Image,'id': x.id}  for x in Picture.objects.all() if x.r_id == id ]
            leno = len(initial)
            if leno == 0:
                for p in instance:
                    p.r_id= id
                    tmp =Picture.objects.all()
                    try:
                        tmp = tmp[len(tmp)-1]
                        id_p = tmp.id+1
                    except:
                        id_p = 0
                    p.id=id_p
                    if(p.Image != ''):
                        p.save()
            else:
                l=[key[5:6] for key in request.FILES.keys()]
                if len(l) > 0 :
                    tmp = 0
                    instance_c=0
                    for x in Picture.objects.all():
                        if x.r_id != record.id :
                            continue
                        if(tmp == int(l[instance_c]) and tmp < leno):
                            x.Image=instance[instance_c].Image
                            instance_c+=1
                            x.save()
                        tmp += 1

                    if int(l[-1]) == leno:
                        instance[instance_c].r_id=id
                        tmp =Picture.objects.all()
                        try:
                            tmp = tmp[len(tmp)-1]
                            id_p = tmp.id+1
                        except:
                            id_p = 0
                        instance[instance_c].id=id_p
                        if(instance[instance_c].Image != ''):
                            instance[instance_c].save()
            initial=[{'Image': x.Image}  for x in Picture.objects.all() if x.r_id == record.id ]
            formset=PictureFormSet(queryset=Picture.objects.none(),initial=initial)
            formset.extra = len(initial)+1
            messages.success(request, f'Medical record updated.')
        else :
            messages.warning(request, f'Medical record not updated.')
    context = {
        'formset':formset,
        'record_f':record_f,
        'Medical_problem': Medical_problem.objects.all(),
        'Medical_record': Medical_record.objects.all(),
        'Picture' :Picture.objects.all(),
        'Ticket' : Ticket.objects.all(),
        'pk':pk,
        'AuthUser': AuthUser.objects.all(),

        'doctor': Doctor.objects.all()
    }
    return render(request, 'hospital_is/medical_ticket_record.html', context)

def medical_problem_edit(request, pk):
    status_f = Status()

    m_form = MedicalProblemCreate()
    medical_problem = get_object_or_404(Medical_problem, id=pk)
    patient = get_object_or_404(AuthUser, id = medical_problem.Patient_ID)
    doctor= get_object_or_404(AuthUser, id = medical_problem.Doctor_ID)
    tmp = ChoosePacient(-1, patient.username)
    tmp2 = ChooseDoctor(-1,doctor.username)
    if request.method == 'POST':
        status_f = request.POST['Status']
        pac = request.POST['Pacient']
        doc = request.POST['Doctor']
        m_form = MedicalProblemUpdateForm(request.POST, request.FILES, instance=medical_problem)
        if m_form.is_valid() :
            if(status_f == '2'):
                for t in Ticket.objects.all():
                    if(t.Medical_problem_ID == pk and t.Status == 0):
                        messages.warning(request, f'All tickets have to be done before closing medical problem.')
                        return HttpResponseRedirect("/medical_problem_edit/" + str(pk))
                medical_problem.Status = 2;

            pac = get_object_or_404(AuthUser, username = pac)
            doc = get_object_or_404(AuthUser, username = doc)

            medical_problem = m_form.save(commit=False)
            medical_problem.Patient_ID=pac.id
            medical_problem.Doctor_ID=doc.id

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
    m_form = MedicalProblemUpdateForm(instance=medical_problem)
    context = {
        'Status' :status_f,
        'pk' : pk,
        'tmp' :tmp,
        'tmp2': tmp2,
        'm_form' : m_form,
        'Record': Medical_record.objects.all(),
        'Medical_problem': Medical_problem.objects.all(),
        'AuthUser': AuthUser.objects.all(),
        'Doctor': Doctor.objects.all(),
        'Ticket': Ticket.objects.all(),
                'Picture' :Picture.objects.all(),

    }

    return render(request, 'hospital_is/medical_problem_edit.html', context)

def medical_problem_create(request):
    tmp = ChoosePacient(-1,'')
    tmp2 = ChooseDoctor(-1,request.user.username)
    m_form = MedicalProblemCreate()

    if request.method == 'POST':
        m_form = MedicalProblemCreate(request.POST, request.FILES)
        if m_form.is_valid():
            medical_problem = m_form.save(commit=False)
            pac = request.POST['Pacient']
            doc = request.POST['Doctor']
            pac = get_object_or_404(AuthUser, username = pac)
            doc = get_object_or_404(AuthUser, username = doc)

            tmp = Medical_problem.objects.all()
            tmp = tmp[len(tmp)-1]
            id = tmp.id + 1

            medical_problem.id = id
            medical_problem.Patient_ID=pac.id
            medical_problem.Doctor_ID=doc.id
            medical_problem.save()
            messages.success(request, f'Medical problem created.')
            if request.user.is_superuser:
                return HttpResponseRedirect("/medical_problems_admin/")
            else:
                return HttpResponseRedirect("/medical_problems_doc/" + str(request.user.id))
        else:
            messages.warning(request, f'Medical problem not updated.')
    m_form = MedicalProblemCreate()
    context = {
    'tmp' :tmp,
    'tmp2': tmp2,
        'm_form' :m_form,
    }
    return render(request, 'hospital_is/medical_problem_create.html', context)

def medical_ticket_create(request,pk):

    t_form = TicketForm()
    user_f = ChooseDoctor(-1,'')
    if request.method == 'POST':
        medical_problem = get_object_or_404(Medical_problem, id=pk)
        if(medical_problem.Status == 2):
            messages.warning(request, f'Ticket   can not be updated when the med problem is finished.')
            return HttpResponseRedirect("/medical_problems_admin/" )
        t_form = TicketForm(request.POST)
        user_f = request.POST['Doctor']
        if(t_form.is_valid() ):
            user_f = get_object_or_404(AuthUser, username=user_f)
            t_form = t_form.save(commit=False)
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

        if c_form.is_valid()  and request.user.is_superuser and request.user.is_staff:
            p_form = request.POST['Insurance']
            insurance_worker = get_object_or_404(AuthUser, username = p_form)
            operation = c_form.save(commit=False)
            operation.creator = insurance_worker.id
            operation.save()
            messages.success(request, f'Compensation operation created.')
            return HttpResponseRedirect("/compensation_operations/")
        elif c_form.is_valid() and request.user.is_superuser and not request.user.is_staff:
            operation = c_form.save(commit=False)
            operation.creator = request.user.id
            operation.save()
            messages.success(request, f'Compensation operation created.')
            return HttpResponseRedirect("/compensation_operations/")
        else:
            messages.warning(request, f'Compensation operation not created.')
    c_form = CompensationOperationsCreate()
    p_form = ChooseInsurance_worker(-1,'')
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
