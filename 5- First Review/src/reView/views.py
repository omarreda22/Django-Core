from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import ViewBlog
from .forms import BlogForm


# @login_required()
def home(request):
    # print(request.get_full_path())
    return HttpResponse('<h1>Hello Tere</h1>')


def blogs(request):
    blogs = ViewBlog.objects.all()
    query = request.GET.get('search')
    if query is not None:
        blogs = blogs.filter(
            Q(title__icontains=query) |
            Q(slug__icontains=query)
        )
    template = 'blogs.html'
    context = {
        'blogs': blogs,
    }
    return render(request, template, context)


def blog(request, slug=None):
    blog = get_object_or_404(ViewBlog, slug=slug)
    template = 'blog.html'
    context = {
        'blog': blog,
    }
    return render(request, template, context)


def create_blog(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.save()
            return redirect(f'/blog/{new_blog.slug}')
    template = 'blog-form.html'
    context = {
        'form': form
    }
    return render(request, template, context)


def edit_blog(request, slug=None):
    blog = get_object_or_404(ViewBlog, slug=slug)
    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        edit = form.save(commit=False)
        edit.save()
        return redirect(f'/edit/blog/{edit.slug}')

    template = 'blog-form.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


def delete_blog(request, slug=None):
    blog = get_object_or_404(ViewBlog, slug=slug)
    if request.method == 'POST':
        blog.delete()
        return redirect('/blogs/')
    template = 'delete-blog.html'
    context = {
        'blog': blog
    }
    return render(request, template, context)


def delete_blog_quick(request, slug=None):
    blog = get_object_or_404(ViewBlog, slug=slug)
    blog.delete()
    return redirect('/blogs/')
