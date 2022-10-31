from django.urls import path
from .views import (
    home,
    auth_login,
    auth_logout,
    auth_register,
    best_register,
)

app_name = 'acc'

urlpatterns = [
    path('', home, name="home"),
    path('login/', auth_login, name='login'),
    path('logout/', auth_logout, name='logout'),
    path('register/', auth_register, name='register'),
    path('best_register/', best_register, name="best_register"),
]
