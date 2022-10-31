from django.urls import path
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.decorators import login_required

from .views import (
    ProductListView,
    ProxyProduct,
    ProductDetailsView,
    RedirectProductDetails,
    RedirectProductBYID,
    ProductCreateView,
    ProductUpdateView,
    UpdateDetailAndUpdate,
    DeleteViewProduct,
)

app_name = 'cbv'

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('team/', RedirectView.as_view(url='/about/'), name='team'),
    path('products/', ProductListView.as_view(), name='products'),
    path('proxy/', ProxyProduct.as_view(), name='proxy'),
    path('a/<slug:slug>/', RedirectProductDetails.as_view(), name='redirect_detail'),
    path('details/<slug:slug>/', RedirectProductDetails.as_view(),
         name='redirect_detail'),
    path('b/<slug:slug>/', RedirectProductDetails.as_view(), name='redirect_detail'),
    path('id/<int:pk>/', RedirectProductBYID.as_view(), name='redirect_detail'),
    path('detail/<slug:slug>/', ProductDetailsView.as_view(), name='detail'),
    path('product/create/', ProductCreateView.as_view(), name='create_product'),
    path('product/update/<slug:slug>/',
         ProductUpdateView.as_view(), name='update_product'),

    path('detail/and/update/<slug:slug>/',
         UpdateDetailAndUpdate.as_view(), name='detail_and_update'),
    path('product/delete/<slug:slug>/',
         DeleteViewProduct.as_view(), name='delete_product'),
]
