from django.shortcuts import render
from django.forms import formset_factory, modelformset_factory
from django.utils.text import slugify
from django.utils import timezone

from .forms import TestForm, PostModelForm
from .models import Post


def home(request):
    form = PostModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()

    if form.has_error:
        print(form.errors.as_json())
        print(form.errors.as_text())

        # data2 = form.errors.as_josn()
        data = form.errors.items()
        # print(data2)
        for key, value in data:
            print(key)
            print(value)
            print(value.as_text())

    template = 'form.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


# initial_values = {
    #     # 'text': "it's test text",
    #     # 'number': 65,
    # }
    # form = TestForm(initial=initial_values)
    # if request.method == 'GET':
    #     form = TestForm(request.GET)
    #     print(request.GET.get('text'))
    #     print(request.GET['text'])
    #     if form.is_valid():
    #         print(form.cleaned_data.get('text'))

    # form = TestForm(request.POST or None)
    # # print(445)
    # if form.is_valid():
    #     print(request.POST.get('text'))
    # # print(565)

    # form = PostModelForm(request.POST or None)
    # if form.is_valid():
    #     print(form['title'])
    #     form['user'] = request.user
    #     form.save()
    #     print(request.POST.get('title'))
    #     print(request.POST.get('user'))
    #     # print(form.user)

    # form = PostModelForm()
    # if request.method == 'POST':
    #     form = PostModelForm(request.POST, user=request.user)
    #     if form.is_valid():
    #         form.save()


# FormSet Custom
# def forms_sets(request):
#     TestFormset = formset_factory(TestForm, extra=2)
#     formset_test = TestFormset(request.POST or None)
#     print('ahmed')
#     if formset_test.is_valid():
#         print('omar')
#         for form in formset_test:
#             print(form.cleaned_data)
#     print('reda')
#     context = {
#         'formset': formset_test,
#     }
#     return render(request, 'forms_sets.html', context)


# form set Model
# def forms_sets(request):
#     PostFormset = modelformset_factory(
#         Post, fields=['title', 'slug', 'publish'])
#     formset_test = PostFormset(request.POST or None)
#     if formset_test.is_valid():
#         for form in formset_test:
#             obj = form.save(commit=False)
#             if form.cleaned_data.get('title'):
#                 print(form.cleaned_data.get('title'))
#                 obj.title = form.cleaned_data.get('title')
#                 obj.slug = slugify(obj.title)
#                 if obj.publish is None:
#                     obj.publish = timezone.now()
#                 # print(form.cleaned_data)
#                 form.save()
#     context = {
#         'formset': formset_test,
#     }
#     return render(request, 'forms_sets.html', context)


# Best form with Model Form
def forms_sets(request):
    PostFormset = modelformset_factory(
        Post, form=PostModelForm)
    formset_test = PostFormset(
        request.POST or None, queryset=Post.objects.filter(user=request.user))
    # request.POST or None, queryset=Post.objects.filter(user__username='omar'))
    if formset_test.is_valid():
        for form in formset_test:
            obj = form.save(commit=False)
            if form.cleaned_data:
                print(form.cleaned_data.get('title'))
                obj.title = form.cleaned_data.get('title')
                obj.slug = slugify(obj.title)
                if obj.publish is None:
                    obj.publish = timezone.now()
                obj.user = request.user
                # print(form.cleaned_data)
                form.save()
    context = {
        'formset': formset_test,
    }
    return render(request, 'forms_sets.html', context)
