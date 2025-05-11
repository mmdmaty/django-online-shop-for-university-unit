from django.shortcuts import render
from django.views import generic
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import *


class AccountDetails(generic.UpdateView):
    template_name = 'store/account_info.html'
    model = get_user_model()
    form_class = UserUpdateForm
    success_url = reverse_lazy('home')
    def get_object(self, queryset = ...):
        return self.request.user
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_model = get_user_model()
        context['account_info'] = user_model.objects.get(
            id=self.request.user.id)
        return context
