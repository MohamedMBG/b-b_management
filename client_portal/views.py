from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from API.models import Client
from .forms import ClientRegistrationForm, ClientLoginForm

def signup(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.set_password(form.cleaned_data['password'])
            client.save()
            login(request, client)
            return redirect('client_dashboard')
    else:
        form = ClientRegistrationForm()
    return render(request, 'client_portal/signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = ClientLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('client_dashboard')
    else:
        form = ClientLoginForm()
    return render(request, 'client_portal/signin.html', {'form': form})

@login_required
def signout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    return render(request, 'client_portal/dashboard.html', {
        'client': request.user,
        'purchases': request.user.achat_set.all()
    })