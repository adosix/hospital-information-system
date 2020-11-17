from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileRegisterForm,AdminUserUpdateForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import AuthUser
from .models import Profile
from hospital_is.models import Admin
from hospital_is.models import Ticket
from hospital_is.models import Medical_record
from hospital_is.models import Medical_problem
from hospital_is.models import Compensation_request
from hospital_is.models import Insurance_worker
from django.contrib.auth.hashers import make_password


def edit_profile(request, username_to_find):

    usr = get_object_or_404(AuthUser, username= username_to_find)
    usr_admin = get_object_or_404(AuthUser, username= request.user)
    profile = get_object_or_404(Profile, user= usr.id)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=usr)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            messages.success(request, f'Your account has been updated!')
            usr_tmp = u_form.save(commit=False)
            if usr_tmp.password != '':
                usr_tmp.password = make_password(usr_tmp.password)
            else:
                usr_tmp.password = usr_admin.password
            usr_tmp.save()
            p_form.save()
        else:
            messages.warning(request, f'Your account hasn\'t been updated!')
            usr = get_object_or_404(AuthUser, username= username_to_find)
            profile = get_object_or_404(Profile, user= usr.id)

    u_form = AdminUserUpdateForm(instance=usr)
    p_form = ProfileUpdateForm(instance=profile)
    context = {
            'u_form': u_form,
            'p_form': p_form,
            'pic_form': profile.get_pic(),
            'username': usr.username,
            'u_id': usr.id,
            }

    return render(request, 'users/edit_profile.html', context)
def delete_profile(request,pk):

    usr = get_object_or_404(AuthUser, id=pk)
    if request.method == "POST" and request.user.is_authenticated and request.user.is_superuser==True and request.user.is_staff==True:



        usr.delete()
        messages.success(request, "User successfully deleted!")
        return HttpResponseRedirect("/users/")
    context= {'usr': usr,              }

    return render(request, 'users/delete_profile.html', context)
def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            created_row = get_object_or_404(Profile, user_id= user.id)
            profile = p_form.save(commit = False)
            created_row.birth_date = profile.birth_date
            created_row.image = profile.image
            created_row.save()


            username = u_form.cleaned_data.get('username')
            messages.success(request, f'Account has been created')
            return redirect('login')
        else:
            messages.warning(request, f'Your account wasn\t created!')
    else:
        u_form = UserRegisterForm()
        p_form = ProfileRegisterForm()
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    usr = get_object_or_404(AuthUser, username= request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            usr_tmp = u_form.save(commit=False)
            if usr_tmp.password != '':
                usr_tmp.password = make_password(usr_tmp.password)
            else:
                usr_tmp.password = usr.password
            messages.success(request, f'Your account has been updated!')
            #return redirect('   ')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
