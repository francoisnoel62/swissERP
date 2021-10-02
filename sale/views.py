from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Sum

from contacts.models import Contact
from payment.forms import PaymentForm
from products.models import Product
from .forms import SaleModelForm, SaleOrderLineFormSet
from .models import SaleOrder, SaleOrderLine
from .utils import render_to_pdf


class SaleOrderCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'sale/create_sale.html'
    form_class = SaleModelForm


class SaleOrderCreateViewWithSOL(LoginRequiredMixin, generic.CreateView):
    template_name = 'sale/create_sale.html'
    form_class = SaleModelForm

    def get_context_data(self, **kwargs):
        data = super(SaleOrderCreateViewWithSOL, self).get_context_data(**kwargs)
        products = Product.objects.filter(created_by=self.request.user)

        if self.request.POST:
            data['sale_order_lines'] = SaleOrderLineFormSet(self.request.POST, instance=self.object)
            for form in data['sale_order_lines']:
                form.fields['product_id'].queryset = products
        else:
            data['sale_order_lines'] = SaleOrderLineFormSet(instance=self.object)
            for form in data['sale_order_lines']:
                form.fields['product_id'].queryset = products

        data['form'].fields['partner_id'].queryset = Contact.objects.filter(user_id=self.request.user)
        return data

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        context = self.get_context_data()
        sale_order_lines = context['sale_order_lines']
        with transaction.atomic():
            self.object = form.save()
            if sale_order_lines.is_valid():
                sale_order_lines.instance = self.object
                sale_order_lines.save()
        return super(SaleOrderCreateViewWithSOL, self).form_valid(form)


class SaleOrderUpdateViewWithSOL(LoginRequiredMixin, generic.UpdateView):
    template_name = 'sale/create_sale.html'
    model = SaleOrder
    form_class = SaleModelForm

    def get_context_data(self, **kwargs):
        data = super(SaleOrderUpdateViewWithSOL, self).get_context_data(**kwargs)
        if self.request.POST:
            data['sale_order_lines'] = SaleOrderLineFormSet(self.request.POST, instance=self.object)
            for form in data['sale_order_lines']:
                form.fields['product_id'].queryset = Product.objects.filter(created_by=self.request.user)
        else:
            data['sale_order_lines'] = SaleOrderLineFormSet(instance=self.object)
            for form in data['sale_order_lines']:
                form.fields['product_id'].queryset = Product.objects.filter(created_by=self.request.user)
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


class SaleOrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'sale/create_sale.html'
    model = SaleOrder
    form_class = SaleModelForm


class SaleOrderIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'sale/sale_listview.html'
    context_object_name = 'sales_list'

    def get_queryset(self):
        return SaleOrder.objects.filter(created_by=self.request.user)


class SaleOrderDetailView(generic.DetailView):
    template_name = 'sale/sale_formview.html'
    model = SaleOrder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PaymentForm()
        context['form'].fields['total'].initial = context['object'].total
        context['form'].fields['date'].initial = datetime.now()
        context['form'].fields['sale_id'].initial = context['object']
        context['form'].fields['created_by'].initial = self.request.user
        return context


class SaleOrderPaymentFormView(SingleObjectMixin, FormView):
    template_name = 'sale/sale_formview.html'
    form_class = PaymentForm
    model = SaleOrder

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            self.object.order_state = 'PD'
            self.object.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('sale_detail', kwargs={'pk': self.object.pk})


class SaleOrderView(View):
    def get(self, request, *args, **kwarg):
        view = SaleOrderDetailView.as_view()
        return view(request, *args, **kwarg)

    def post(self, request, *args, **kwargs):
        view = SaleOrderPaymentFormView.as_view()
        return view(request, *args, **kwargs)


class SaleOrderDeleteView(LoginRequiredMixin, generic.DeleteView):
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
    return redirect(order)


def clean_sol(request, order_id):
    order = SaleOrder.objects.get(pk=order_id)
    sol = SaleOrderLine.objects.filter(sale_order_id=order_id).values('product_id').annotate(quantity=Sum('quantity'))
    for item in sol:
        prod = Product.objects.filter(created_by=request.user).get(pk=item['product_id'])
        qty = item['quantity']
        total = prod.price * qty
        new_sol = SaleOrderLine(product_id=prod, quantity=qty, sol_total=total, sale_order_id=order)
        new_sol.save()
        old_sol = SaleOrderLine.objects.filter(sale_order_id=order_id, quantity__lt=qty)
        for element in old_sol:
            element.delete()
    order.order_state = 'CL'
    order.save()
    return redirect(order)


def generate_pdf(request, order_id):
    order = SaleOrder.objects.get(pk=order_id)
    template = get_template('sale/invoice_pdf.html')
    context = {
        "order": order,
        "user": request.user,
    }
    html = template.render(context)
    pdf = render_to_pdf('sale/invoice_pdf.html', context)

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "inline; filename='%s'" % (filename)
        download = request.GET.get("download")
        if download:
            content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")
