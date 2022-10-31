from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm


def home(request):
    return render(request, 'home.html')


def auth_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, f'You logged in successfully as {user.username}')
            return redirect("acc:home")
        else:
            messages.error(request, 'Some information Wrong!')
            return redirect("acc:login")

    template = 'auth/login.html'
    context = {}
    return render(request, template, context)


def auth_logout(request):
    logout(request)
    messages.success(request, 'You Logout, Come Back Soon!')
    return redirect('acc:login')


def auth_register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            messages.success(
                request, f'You are register successfully! as {new_user.username}')
            return redirect('acc:login')
        else:
            messages.error(request, 'Some information Wrong!')
            return redirect('acc:register')

    template = 'auth/register.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


def best_register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            messages.success(
                request, f'You are Create New User successfully! as {new_user.username}')
            return redirect('acc:login')
        else:
            messages.error(request, 'some information wrong')
            return redirect("acc:best_register")
    template = 'auth/best_register.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
