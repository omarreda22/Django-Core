from django.urls import path
from django.views.generic import TemplateView

from .views import (
    home,
    blogs,
    blog,
    create_blog,
    edit_blog,
    delete_blog,
    delete_blog_quick
)

app_name = 'reView'

urlpatterns = [
    path('', home, name='home'),
    path('team/', TemplateView.as_view(template_name='team.html'), name='team'),
    path('blogs/', blogs, name='blogs'),
    path('blog/<slug:slug>/', blog, name='blog'),
    path('create/blog/', create_blog, name='create_blog'),
    path('edit/blog/<slug:slug>/', edit_blog, name='edit_blog'),
    path('delete/blog/<slug:slug>/', delete_blog, name="delete_blog"),
    path('delete/quick/blog/<slug:slug>/',
         delete_blog_quick, name="delete_quick"),
]
