from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from next_prev import next_in_order, prev_in_order

from .models import SaleOrder, SaleOrderLine


# SALE ORDER
class SaleOrderIndexView(generic.ListView):
    template_name = ''
    context_object_name = 'sales_list'
    queryset = SaleOrder.objects.all()


class SaleOrderDetailView(generic.DetailView):
    template_name = ''
    model = SaleOrder


# SALE ORDER LINE
class SaleOrderLineIndexView(generic.ListView):
    template_name = ''
    context_object_name = 'sale_orders_list'
    queryset = SaleOrderLine.objects.all()


class SaleOrderLineDetailView(generic.DetailView):
    template_name = ''
    model = SaleOrderLine
