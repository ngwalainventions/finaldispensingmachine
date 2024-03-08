# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from . forms import SignUpForm, EmailAuthenticationForm  #, UserLoginForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # return redirect('welcome')  # Redirect to your home page
            return redirect('index')  # Redirect to your home page
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def user_list_view(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})

