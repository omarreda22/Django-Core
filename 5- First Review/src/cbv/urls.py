from django.urls import path
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required

from .views import (
    ListViewDisplay,
    MixinsTest,
    RedirectClass,
    DetailProd,
    CreateProd,
    UpdateProd,
    DeleteProd,
)

app_name = 'cbv'


urlpatterns = [
    path('', login_required(TemplateView.as_view(
        template_name='home.html')), name='home'),
    path('home_redirect/', RedirectView.as_view(url='/cbv/'),
         name='redirect_name'),
    path('display/', ListViewDisplay.as_view(), name='display'),
    path('mixins_test/', MixinsTest.as_view(), name='mixins_test'),
    path('red/<slug:slug>', RedirectClass.as_view(), name='red'),
    path('detail/<slug:slug>', DetailProd.as_view(), name='detail'),
    path('create/', CreateProd.as_view(), name='create_prod'),
    path('update/<slug:slug>', UpdateProd.as_view(), name='update'),
    path('delete/<slug:slug>', DeleteProd.as_view(), name='delete'),
]
