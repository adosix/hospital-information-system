from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import AuthUser
from .models import Profile



def edit_profile(request, username_to_find):

    usr = get_object_or_404(AuthUser, username= username_to_find)
    profile = get_object_or_404(Profile, user= usr.id)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=usr)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            messages.success(request, f'Your account has been updated!')
            u_form.save()
            p_form.save()
            usr = get_object_or_404(AuthUser, username= username_to_find)
            
            usr.set_password(u_form.password)
            usr.save()
        else:
            messages.warning(request, f'Your account hasn\'t been updated!')
            usr = get_object_or_404(AuthUser, username= username_to_find)
            profile = get_object_or_404(Profile, user= usr.id)

    u_form = UserUpdateForm(instance=usr)
    p_form = ProfileUpdateForm(instance=profile)
    context = {
            'u_form': u_form,
            'p_form': p_form,
            'pic_form': profile.get_pic(),
            'username': usr.username,
            }

    return render(request, 'users/edit_profile.html', context)
    

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
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
