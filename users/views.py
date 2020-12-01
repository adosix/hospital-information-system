import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileRegisterForm,AdminUserUpdateForm,UserRoleForm,ChooseDoctor,PatientWH
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

from .models import AuthUser
from .models import Profile
from hospital_is.models import Admin
from hospital_is.models import Insurance_worker
from hospital_is.models import Doctor
from hospital_is.models import Patient
from hospital_is.models import Ticket
from hospital_is.models import Medical_record
from hospital_is.models import Medical_problem
from hospital_is.models import Compensation_request
from hospital_is.models import Insurance_worker
from django.contrib.auth.hashers import make_password
from datetime import datetime

def edit_profile(request, username_to_find):
    if (request.user.is_staff == False):
        return render(request, 'hospital_is/405.html', {})

    try:
        usr = get_object_or_404(AuthUser, username= username_to_find)
        if (request.user.is_superuser == False and (usr.is_staff or usr.is_superuser) ):
            return render(request, 'hospital_is/405.html', {})
    except:
        return render(request, 'hospital_is/404.html', {})

    role_form = UserRoleForm()
    if usr.is_staff and usr.is_superuser:
        role_form.fields['Role'].initial=[0]
        tmp = get_object_or_404(Admin, id=usr.id)
    if usr.is_staff and not usr.is_superuser:
        role_form.fields['Role'].initial=[3]
        tmp = get_object_or_404(Doctor, id=usr.id)
    if not usr.is_staff and usr.is_superuser:
        role_form.fields['Role'].initial=[2]
        tmp = get_object_or_404(Insurance_worker, id=usr.id)
    if not usr.is_staff and not usr.is_superuser:
        role_form.fields['Role'].initial=[1]
        tmp = get_object_or_404(Patient, id=usr.id)
    pass_tmp = usr.password
    usr_admin = get_object_or_404(AuthUser, username= request.user)
    profile = get_object_or_404(Profile, user= usr.id)
    if tmp.whoami() == "Patient" :

        hw_form = PatientWH(instance=tmp)
    else:
        hw_form = PatientWH()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=usr)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=profile)
        if tmp.whoami() == "Patient" :
            hw_form = PatientWH(request.POST,instance=tmp)
        if u_form.is_valid() and p_form.is_valid():

            if 'del' in request.POST:
                usr = u_form.save(commit=False)
                usr.delete()
                messages.success(request, f'User has been deleted!')
                return HttpResponseRedirect("/users/")
            if 'del1' in request.POST:
                return HttpResponseRedirect("/move_medical_problems/" + str(usr.id))
                #usr = u_form.save(commit=False)
                #usr.delete()
                #messages.success(request, f'User has been deleted!')
            if tmp.whoami() == "Patient" :
                hw_form = hw_form.save(commit=False)
                pat = get_object_or_404(Patient, id = usr.id )
                try:
                    hw_form.height<0
                except Exception as e:
                    hw_form.height = 0
                try:
                    hw_form.weight<0
                except Exception as e:
                    hw_form.weight = 0
                if(hw_form.height < 0 or hw_form.height > 500 or hw_form.weight < 0 and hw_form.weight > 800):
                    messages.warning(request, f'An account hasn\'t been updated!')
                    u_form = UserUpdateForm(instance=request.user)
                    p_form = ProfileUpdateForm(instance=request.user.profile)
                    hw_form = PatientWH(request.POST,instance=tmp)
                    context = {
                    'Patient' : Patient.objects.all(),
                    'Auth' : AuthUser.objects.all(),
                    'hw_form' : hw_form,
                    'pk':pk,
                    'u_id': usr.id,
                        'u_form': u_form,
                        'p_form': p_form
                    }

                    return render(request, 'users/profile.html', context)
                pat.height = hw_form.height
                pat.weight = hw_form.weight

                pat.save()
            usr_tmp = u_form.save(commit=False)

            if usr_tmp.password != '':
                usr_tmp.password = make_password(usr_tmp.password)
            else:
                usr_tmp.password = pass_tmp
            usr_tmp.save()
            p=p_form.save(commit=False)
            max = datetime.now().date()
            min = datetime(1900,1,1).date()
            if(p.birth_date >= max or p.birth_date<= min ):
                messages.warning(request, f'An account hasn\'t been updated!')
                u_form = UserUpdateForm(instance=request.user)
                p_form = ProfileUpdateForm(instance=request.user.profile)
                if tmp.whoami() == "Patient" :
                    hw_form = PatientWH(request.POST,instance=tmp)
                context = {
                'Patient' : Patient.objects.all(),
                'Auth' : AuthUser.objects.all(),
                'hw_form' : hw_form,
                'u_id': usr.id,
                'pk':pk,
                    'u_form': u_form,
                    'p_form': p_form
                }

                return render(request, 'users/profile.html', context)

            p.save()
            messages.success(request, f'An account has been updated!')
        else:
            messages.warning(request, f'An account hasn\'t been updated!')
            usr = get_object_or_404(AuthUser, username= username_to_find)
            profile = get_object_or_404(Profile, user= usr.id)

    u_form = AdminUserUpdateForm(instance=usr)
    p_form = ProfileUpdateForm(instance=profile)
    role_form = UserRoleForm()
    if tmp.whoami() == "Patient" :

        hw_form = PatientWH(instance=tmp)
    else:
        hw_form = PatientWH()
    if usr.is_staff and usr.is_superuser:
        role_form.fields['Role'].initial=[0]
    if usr.is_staff and not usr.is_superuser:
        role_form.fields['Role'].initial=[3]
    if not usr.is_staff and usr.is_superuser:
        role_form.fields['Role'].initial=[2]
    if not usr.is_staff and not usr.is_superuser:
        role_form.fields['Role'].initial=[1]

    context = {
    'Patient' : Patient.objects.all(),
    'Auth' : AuthUser.objects.all(),
            'hw_form' : hw_form,
            'u_form': u_form,
            'p_form': p_form,
                'role_form' :role_form,
            'pic_form': profile.get_pic(),
            'username': usr.username,
            'u_id': usr.id,
            'usr': usr,
            }

    return render(request, 'users/edit_profile.html', context)
def move_medical_problems(request,pk):
    if request.user.is_staff == False or request.user.is_superuser == False:
        return render(request, 'hospital_is/405.html', {})
    try:
        usr = get_object_or_404(AuthUser, id=pk)
        doc = get_object_or_404(Doctor, id=pk)
    except:
        return render(request, 'hospital_is/404.html', {})
    u_form = ChooseDoctor(pk,'')
    if request.method == 'POST':
        usr = request.POST['Doctor']
        doc = get_object_or_404(AuthUser, id=pk)
        new_doc = get_object_or_404(AuthUser, username=usr)
        tmp = get_object_or_404(AuthUser, username="doc do not exist")
        for p in Medical_problem.objects.all():
            if p.Doctor_ID == pk:
                p.Doctor_ID = new_doc.id
                p.save()
        for t in Ticket.objects.all():
            if t.Doctor_ID == doc.id:
                t.Doctor_ID = tmp.id
                t.Status = 2
                t.save()
        doc.delete()
        messages.success(request, f'User has been deleted!')
        return HttpResponseRedirect("/users/")
    context = {
            'u_form': u_form,
            'AuthUser': AuthUser.objects.all(),
            }
    return render(request, 'users/move_medical_problems.html', context)

def register(request):
    if  request.user.is_staff == False :
        return render(request, 'hospital_is/405.html', {})
    role_form = UserRoleForm()
    hw_form = PatientWH()
    if request.method == 'POST':

        u_form = UserRegisterForm(request.POST)
        p_form = ProfileRegisterForm(request.POST,
                                   request.FILES)
        hw_form = PatientWH(request.POST)
        try:
            role_form = request.POST['Role']
        except:
            pass
        if u_form.is_valid() and p_form.is_valid():

            user = u_form.save(commit=False)
            profile=p_form.save(commit=False)
            #getting username
            i = 0
            while True:

                stop = False
                user.username = user.last_name[0 : 5]+str(i)
                for u in  AuthUser.objects.all():
                    if u.username == user.username:
                        stop = False
                        i += 1
                        break
                    stop = True
                if stop == True:
                    break


            max = datetime.now().date()
            min = datetime(1900,1,1).date()
            if(profile.birth_date >= max or profile.birth_date<= min ):
                messages.warning(request, f'An account wasnt created!')
                u_form = UserUpdateForm(instance=request.user)
                p_form = ProfileUpdateForm(instance=request.user.profile)
                hw_form = PatientWH()
                context = {
                        'hw_form': hw_form,

                'pk':pk,
                    'u_form': u_form,
                    'p_form': p_form
                }

                return render(request, 'users/register.html', context)
            if(request.user.is_superuser):
                if(role_form == '0'):
                    user.is_superuser = True
                    user.is_staff = True
                    user.save()
                    Admin.objects.create(id = user.id)
                    if profile.image == "default.jpg":
                        profile.image = "default_admin.png"
                elif(role_form == '1'):
                    user.is_superuser = False
                    user.is_staff = False
                    user.save()
                    Patient.objects.create(id = user.id)
                    if profile.image == "default.jpg":
                        profile.image = "default_user.png"
                elif(role_form == '2'):
                    user.is_superuser = True
                    user.is_staff = False
                    user.save()
                    Insurance_worker.objects.create(id = user.id)
                    if profile.image == "default.jpg":
                        profile.image = "default_ins.png"
                else:
                    user.is_superuser = False
                    user.is_staff = True
                    user.save()
                    Doctor.objects.create(id = user.id)
                    if profile.image == "default.jpg":
                        profile.image = "default_doc.jpg"
            else:
                user.save()
                hw_form = hw_form.save(commit=False)
                try:
                    hw_form.height<0
                except Exception as e:
                    hw_form.height = 0
                try:
                    hw_form.weight<0
                except Exception as e:
                    hw_form.weight = 0
                if(hw_form.height < 0 or hw_form.height > 500 or hw_form.weight < 0 and hw_form.weight > 800):
                    messages.warning(request, f'An account was not created!')
                    u_form = UserUpdateForm(instance=request.user)
                    p_form = ProfileUpdateForm(instance=request.user.profile)
                    hw_form = PatientWH()
                    context = {
                            'hw_form': hw_form,

                    'pk':pk,
                        'u_form': u_form,
                        'p_form': p_form
                    }

                    return render(request, 'users/register.html', context)
                Patient.objects.create(id = user.id, height=hw_form.height, weight=hw_form.weight)
                if profile.image == "default.jpg":
                    profile.image = "default_user.png"
            created_row = get_object_or_404(Profile, user_id= user.id)
            created_row.birth_date = profile.birth_date
            created_row.image = profile.image
            created_row.save()

            #TOGO
            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Account has been created')
            return redirect('/users/')
        else:
            messages.warning(request, f'Your account wasnt created!')
            u_form = UserRegisterForm()
            p_form = ProfileRegisterForm()
            role_form = UserRoleForm()
            hw_form = PatientWH()
    else:
        u_form = UserRegisterForm()
        p_form = ProfileRegisterForm()
        role_form = UserRoleForm()
    context = {
        'hw_form': hw_form,
        'role_form' :role_form,
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/register.html', context)


@login_required
def profile(request,pk):
    try:

        usr = get_object_or_404(AuthUser, id=pk)
    except:
        return render(request, 'hospital_is/404.html', {})
    if request.user.id != pk:
        return render(request, 'hospital_is/405.html', {})
    pass_tmp = usr.password
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=usr)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        try:
            hw_form = PatientWH(request.POST, instance=get_object_or_404(Patient, id=request.user.id))
        except Exception as e:
            hw_form = PatientWH()

        if u_form.is_valid() and p_form.is_valid():
            logout_f=False
            usr_tmp = u_form.save(commit=False)
            if usr_tmp.password != '':
                usr_tmp.password = make_password(usr_tmp.password)
                logout_f=True
            else:
                usr_tmp.password = pass_tmp
            p=p_form.save(commit=False)
            max = datetime.now().date()
            min = datetime(1900,1,1).date()
            if(p.birth_date >= max or p.birth_date<= min ):
                messages.warning(request, f'Your account wasnt updated!')
                u_form = UserUpdateForm(instance=request.user)
                p_form = ProfileUpdateForm(instance=request.user.profile)
                try:
                    hw_form = PatientWH(instance=get_object_or_404(Patient, id=request.user.id))
                except Exception as e:
                    hw_form = PatientWH()
                context = {
                    'pk':pk,
                        'u_form': u_form,
                        'p_form': p_form,
                        'hw_form': hw_form
                    }

                return render(request, 'users/profile.html', context)
            hw_form = hw_form.save(commit=False)
            try:
                hw_form.height<0
            except Exception as e:
                hw_form.height = 0
            try:
                hw_form.weight<0
            except Exception as e:
                hw_form.weight = 0
            if(hw_form.height < 0 or hw_form.height > 500 or hw_form.weight < 0 and hw_form.weight > 800):
                messages.warning(request, f'An account was not created!')
                u_form = UserUpdateForm(instance=request.user)
                p_form = ProfileUpdateForm(instance=request.user.profile)
                try:
                    hw_form = PatientWH(instance=get_object_or_404(Patient, id=request.user.id))
                except Exception as e:
                    hw_form = PatientWH()
                context = {
                    'pk':pk,
                        'u_form': u_form,
                        'p_form': p_form,
                        'hw_form': hw_form
                    }

                return render(request, 'users/profile.html', context)
            hw_form.id = request.user.id
            hw_form.save()
            p.save()
            messages.success(request, f'Your account has been updated!')
            #return redirect('   ')
            usr_tmp.save()
            if logout_f:

                return render(request, 'users/login.html', {})
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    try:
        hw_form = PatientWH(instance=get_object_or_404(Patient, id=request.user.id))
    except Exception as e:
        hw_form = PatientWH()

    context = {
    'pk':pk,
        'u_form': u_form,
        'p_form': p_form,
        'hw_form': hw_form
    }

    return render(request, 'users/profile.html', context)
