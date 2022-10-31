from django.urls import path
from .views import main, create_form

app_name = 'mdls'

urlpatterns = [
    path('', main, name='main'),
    path('create/', create_form, name='create_form'),
]
