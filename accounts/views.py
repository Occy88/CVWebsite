
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# Create your views here.

def home(request):
    numbers= {1,2,3,4,5}
    name= 'Octavio'
    args={'myName': name}
    return render(request, 'accounts/templates/accounts/home.html',args)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/account/')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/templates/accounts/register.html', {'form': form})
