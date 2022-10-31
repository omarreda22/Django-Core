from django.shortcuts import render
from django.views.generic import (
    ListView,
    RedirectView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

from mdls.models import Main
from .Mixins import CustomMixins
from mdls.forms import MainForm


class ListViewDisplay(LoginRequiredMixin, ListView):
    model = Main
    template_name = 'list_view.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['omar'] = 'reda'
        return context


class MixinsTest(CustomMixins, ListView):
    model = Main
    template_name = 'mixins_test.html'
    title = 'Main Title'
    add = 'Add'


class DetailProd(DetailView):
    model = Main
    template_name = 'detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print(self.kwargs)
        return context


class RedirectClass(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        url = self.kwargs.get('slug')
        print(url)
        return f'/cbv/detail/{url}'


class CreateProd(CreateView):
    form_class = MainForm
    template_name = 'create_prod.html'


class UpdateProd(UpdateView):
    form_class = MainForm
    template_name = 'create_prod.html'
    model = Main

    # def get_queryset(self):
    #     return super().get_queryset()


class DeleteProd(DeleteView):
    template_name = 'cbv_delete.html'
    model = Main

    def get_success_url(self):
        return f'/cbv/display/'
