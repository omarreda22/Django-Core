from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model, logout

from .forms import UserCreationForm, UserLogin
from .models import NewUser

User = get_user_model()


def user_register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        # username = form.cleaned_data.get('username')
        # user = NewUser.objects.get(username=username)
        # user.is_active = False
        # user.save()
        return redirect("accounts:register")
    template_name = 'register.html'
    context = {
        'form': form,
    }
    return render(request, template_name, context)


def user_login(request):
    form = UserLogin(request.POST or None)
    if form.is_valid():
        user = form.cleaned_data.get('user_obj')
        # user = User.objects.get(username__iexact=username)
        login(request, user)
        return redirect("accounts:home")

    template_name = 'login.html'
    context = {
        'form': form,
    }
    return render(request, template_name, context)


def user_logout(request):
    logout(request)
    return redirect('accounts:login')
