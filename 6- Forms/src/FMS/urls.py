from django.urls import path

from .views import home, forms_sets

app_name = 'fms'

urlpatterns = [
    path('', home, name='home'),
    path('forms_sets/', forms_sets, name='forms_sets'),
]
