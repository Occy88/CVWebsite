
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from accounts.forms import (
    RegistrationForm,
    EditProfileForm

)
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    numbers= {1,2,3,4,5}
    name= 'Octavio'
    args={'myName': name}
    return render(request, 'accounts/templates/registration/home.html',args)
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/account')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/templates/registration/register.html', {'form': form})
def view_profile(request):
    args = {'user':request.user}
    return render(request,'accounts/templates/registration/profile.html',args)

def edit_profile(request):
    if request.method == 'POST':
        form=EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/account/profile')
    else:
        form= EditProfileForm(instance=request.user)
        args={'form':form}
        return render(request,'accounts/templates/registration/eddit_profile.html',args)

def change_password(request):
    if request.method == 'POST':
        form=PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('/account/profile')
        else:
            return redirect('/account/change-password')
    else:
        form= PasswordChangeForm(user=request.user)
        args={'form':form}
        return render(request,'accounts/templates/registration/change_password.html',args)
