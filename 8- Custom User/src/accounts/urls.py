from django.urls import path
from django.views.generic import TemplateView

from .views import (
    user_register,
    user_login,
    user_logout
)

app_name = 'accounts'

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
