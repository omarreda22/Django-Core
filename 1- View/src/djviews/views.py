from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q

from .models import PostModel
from .forms import PostModelForm


def post_model_list_view(request):
    qs = PostModel.objects.all()
    template = "list-view.html"

    query = request.GET.get('q')
    if query is not None:
        qs = qs.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
        template = "search_result.html"

        # if request.user.is_authenticated:
        # 	template = "list-view.html"
        # else:
        # 	template = "list-view-public.html"
        # raise Http404
        # return HttpResponse("Some Data")

    context = {
        'qs': qs,
    }
    return render(request, template, context)

# CRUD[Create - Retrieve - Update - Delete ]


def retrieve_view(request, name=None):
    qs = get_object_or_404(PostModel, title=name)
    template = "CRUD/retrieve_view.html"
    context = {
        'qs': qs,
    }
    return render(request, template, context)


# def create_view(request):
# 	# POST -> we are send post data to back
# 	form = PostModelForm()
# 	if request.method == "POST":

# 		form = PostModelForm(request.POST)
# 		if form.is_valid():
# 			blog = form.save(commit=False)
# 			blog.save()
# 			messages.success(request, "New Blog Post Successfully!")

# 			# if you dont put "/" he will move to different link
# 			return redirect(f"/blog/retrieve/{blog.id}")


# 	template = "CRUD/create_view.html"
# 	context = {
# 		'form': form,
# 	}
# 	return render(request, template, context)


def create_blog(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.save()
            messages.success(request, 'New Blog Posted Successfully!')
            return redirect(f'/blog/retrieve/{new_blog.title}')
    form = PostModelForm()
    template = "CRUD/create_view.html"
    context = {
        'form': form,
    }
    return render(request, template, context)

# instance meaning showing data


def edit_blog(request, name=None):
    blog = get_object_or_404(PostModel, title=name)
    # form = PostModelForm(instance=blog)
    form = PostModelForm(request.POST or None, instance=blog)
    # if request.method == "POST":
    # form = PostModelForm(request.POST, instance=blog)
    if form.is_valid():
        edit_blog = form.save(commit=False)
        edit_blog.save()
        messages.success(request, "Edit Blog Successfully!")
        return redirect(f"/blog/retrieve/{edit_blog.title}/")

    template = "CRUD/edit_blog.html"
    context = {
        'object': blog,
        'form': form,
    }
    return render(request, template, context)


def delete_blog(request, name=None):
    blog = get_object_or_404(PostModel, title=name)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, "Blog Delete Successfully!")
        return redirect("blog:post_model_list_view")
    template = "CRUD/delete_blog.html"
    context = {
        'blog': blog
    }
    return render(request, template, context)


def delete_quickly(request, name=None):
    blog = get_object_or_404(PostModel, title=name)
    messages.success(request, "Blog Delete Successfully!")
    blog.delete()
    return redirect("blog:post_model_list_view")
