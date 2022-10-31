from django import forms

from .models import ViewBlog


class BlogForm(forms.ModelForm):
    class Meta:
        model = ViewBlog
        fields = ['title', 'slug']
