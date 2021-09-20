from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import generic

from payment.forms import PaymentForm


class PaymentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'sale/sale_formview.html'
    form_class = PaymentForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
