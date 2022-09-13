from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from apps.payment.forms import PaymentForm
from apps.payment.models import Payment


class PaymentListView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    template_name = 'payment/payment_listview.html'
    context_object_name = 'payments_list'

    def get_queryset(self):
        return Payment.objects.filter(created_by=self.request.user)


class PaymentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'sale/sale_formview.html'
    form_class = PaymentForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class PaymentDetailView(LoginRequiredMixin, generic.DetailView):
    pass
