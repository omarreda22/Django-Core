from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    RedirectView,
    CreateView,
    UpdateView,
    DeleteView,
)
# from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from .models import Product, ProxyProduct
from .maxins import ProductMixins
from .forms import ProductModelForm


class ProxyProduct(ProductMixins, ListView):
    model = ProxyProduct
    template_name = 'cbv/pyproducts.html'
    title = 'Proxy Model'
    omar = 'Ali'


class ProductListView(ProductMixins, ListView):
    model = Product
    template_name = 'cbv/pyproducts.html'
    title = 'All Products'
    # For tempates we can use the default template
    # <app_name>/<model_name>_<view_name> = cbv/product_view

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['omar'] = 'reda'
    #     print(context)
    #     return context


class LoginRequiredMixins():
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        super().dispatch(*args, **kwargs)


class ProductDetailsView(LoginRequiredMixin, DetailView):
    model = Product
    print('red')
    template_name = 'cbv\detail.html'
    print('omar')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(self.kwargs)
        print(self.kwargs.get('slug'))
        print(context)
        return context


class RedirectProductDetails(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url = self.kwargs.get('slug')
        # obj = get_object_or_404(Product, slug=url)
        # return f'/detail/{obj.slug}/'

        return f'/detail/{url}/'


class RedirectProductBYID(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(Product, pk=pk)
        return f'/detail/{obj.slug}'


class ProductCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductModelForm
    template_name = "cbv/forms.html"
    # success_url = '/products/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        # obj = form.save(commit=False)
        # obj.user = self.request.user
        # obj.save()
        return super().form_valid(form)

    # def form_invalid(self, form):
    #     return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProductModelForm
    # model = Product
    template_name = 'cbv/update.html'

    # this do in sure that the same user will update
    def get_queryset(self):
        obj = Product.objects.filter(user=self.request.user)
        return obj

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     return super().form_valid(form)


class UpdateDetailAndUpdate(LoginRequiredMixin, UpdateView):
    form_class = ProductModelForm
    template_name = "cbv/detail.html"  # this template same detail template

    def get_queryset(self):
        obj = Product.objects.filter(user=self.request.user)
        return obj

    def get_success_url(self):
        # obj = Product.objects.get(slug=self.kwargs.get('slug'))
        # return f'/detail/and/update/{obj.slug}'
        return self.object.get_update_url()


class DeleteViewProduct(LoginRequiredMixin, DeleteView):
    template_name = 'cbv/form-delete.html'

    def get_queryset(self):
        obj = Product.objects.filter(user=self.request.user)
        return obj

    def get_success_url(self):
        return '/products/'
