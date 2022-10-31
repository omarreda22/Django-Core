from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib import messages

from .forms import MainForm


def main(request):
    template = 'main.html'
    context = {

    }
    return render(request, template, context)


def create_form(request):
    form = MainForm()
    if request.method == 'POST':
        print('asd')
        form = MainForm(request.POST)
        if form.is_valid():
            print('111')
            new_mdl = form.save(commit=False)
            new_mdl.save()
            return redirect('mdls:main')
        # else:
        #     raise ValidationError("You Must don't have 'Omar' in Title field")
        # else:
        #     messages.error(request, "some information error")
        #     return redirect(request.get_full_path())
    template = 'create-main.html'
    context = {
        'form': form
    }
    return render(request, template, context)
