from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import SaleModelForm, SaleOrderLineFormSet
from .models import SaleOrder


# SALE ORDER
class SaleOrderCreateView(generic.CreateView):
    template_name = 'sale/create_sale.html'
    form_class = SaleModelForm


class SaleOrderCreateViewWithSOL(generic.CreateView):
    template_name = 'sale/create_sale.html'
    form_class = SaleModelForm

    def get_context_data(self, **kwargs):
        data = super(SaleOrderCreateViewWithSOL, self).get_context_data(**kwargs)
        if self.request.POST:
            data['sale_order_lines'] = SaleOrderLineFormSet(self.request.POST)
        else:
            data['sale_order_lines'] = SaleOrderLineFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        sale_order_lines = context['sale_order_lines']
        with transaction.atomic():
            self.object = form.save()

            if sale_order_lines.is_valid():
                sale_order_lines.instance = self.object
                sale_order_lines.save()
        return super(SaleOrderCreateViewWithSOL, self).form_valid(form)


class SaleOrderUpdateViewWithSOL(generic.UpdateView):
    template_name = 'sale/create_sale.html'
    model = SaleOrder
    form_class = SaleModelForm

    def get_context_data(self, **kwargs):
        data = super(SaleOrderUpdateViewWithSOL, self).get_context_data(**kwargs)
        if self.request.POST:
            data['sale_order_lines'] = SaleOrderLineFormSet(self.request.POST, instance=self.object)
        else:
            data['sale_order_lines'] = SaleOrderLineFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        sale_order_lines = context['sale_order_lines']
        with transaction.atomic():
            self.object = form.save()

            if sale_order_lines.is_valid():
                sale_order_lines.instance = self.object
                sale_order_lines.save()
        return super(SaleOrderUpdateViewWithSOL, self).form_valid(form)


class SaleOrderUpdateView(generic.UpdateView):
    template_name = 'sale/create_sale.html'
    model = SaleOrder
    form_class = SaleModelForm


class SaleOrderIndexView(generic.ListView):
    template_name = 'sale/sale_listview.html'
    context_object_name = 'sales_list'
    queryset = SaleOrder.objects.all()


class SaleOrderDetailView(generic.DetailView):
    template_name = 'sale/sale_formview.html'
    model = SaleOrder


class SaleOrderDeleteView(generic.DeleteView):
    model = SaleOrder
    success_url = reverse_lazy('sales')

    def delete(self, request, *args, **kwargs):
        deleted_sale = super(SaleOrderDeleteView, self).get_object()
        messages.success(self.request, f"{deleted_sale.name} was removed from DB ")
        return super(SaleOrderDeleteView, self).delete(request, *args, **kwargs)


def confirm_order(request, order_id):
    order = SaleOrder.objects.get(pk=order_id)
    order.order_state = 'CF'
    order.save()
    return redirect('sales')