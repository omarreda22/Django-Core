from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import RegisterForm


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, f'You logged in successfully as {user.username}')
            return redirect('reView:blogs')
        else:
            messages.error(request, 'Your information is wrong')
            return redirect('accounts:user_login')
    template = 'login.html'
    context = {

    }
    return render(request, template, context)


def user_logout(request):
    logout(request)
    messages.success(request, 'You Logout Successfully!')
    return redirect('accounts:user_login')


def user_register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            messages.success(request, 'You are Register succuflly')
            return redirect('reView:blogs')

    template = 'register-form.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
