from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from next_prev import next_in_order, prev_in_order

from .models import SaleOrder, SaleOrderLine
from .forms import SaleModelForm


# SALE ORDER
class SaleOrderCreateView(generic.CreateView):
    template_name = 'sale/create_sale.html'
    form_class = SaleModelForm


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
