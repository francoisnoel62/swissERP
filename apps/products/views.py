from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import PassModelForm, ProductModelForm, SubModelForm
from .models import Product, Subscription, UnitPass
from ..sessions.models import Session


class ProductListView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    template_name = 'product/products_listview.html'
    context_object_name = 'products_list'

    def get_queryset(self):
        if self.request.GET.get("filter") is not None:
            query = self.request.GET.get("filter")
            object_list = Product.objects.filter(
                Q(student__name__icontains=query) | Q(student__lastname__icontains=query)
            ).filter(user_id=self.request.user)
            return object_list
        elif self.request.GET.get("sub") is not None:
            object_list = Product.objects.exclude(subscription__isnull=True).filter(user_id=self.request.user)
            return object_list
        elif self.request.GET.get("pass") is not None:
            object_list = Product.objects.exclude(unitpass__isnull=True).filter(user_id=self.request.user)
            return object_list
        else:
            return Product.objects.filter(user_id=self.request.user)


class ProductCreatePassView(LoginRequiredMixin, generic.CreateView):
    template_name = 'product/create_pass.html'
    form_class = PassModelForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Create pass success')
        return super(ProductCreatePassView, self).form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Create pass failed')
        return response


class ProductCreateSubView(LoginRequiredMixin, generic.CreateView):
    template_name = 'product/create_subscription.html'
    form_class = SubModelForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Create subscription success')
        return super(ProductCreateSubView, self).form_valid(form)

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, 'Create subscription failed')
        return response


class PassUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'product/create_pass.html'
    form_class = PassModelForm
    model = UnitPass


class SubscriptionUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'product/create_subscription.html'
    form_class = SubModelForm
    model = Subscription


class ProductDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Product
    success_url = reverse_lazy("products")

    def form_valid(self, form):
        messages.success(self.request, f"{self.object} was deleted ✅ ")
        return super(ProductDeleteView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError as e:
            messages.error(self.request, f"⛔️ Enable to delete this product as it is used in other relations !")
            for x in e.args[1]:
                messages.info(self.request, f"{x}")
            return redirect(self.success_url)


def update_subscription(request):
    subscriptions = Subscription.objects.all().filter(user_id=request.user)
    for sub in subscriptions:
        sub.current_credits = sub.classes_by_week
        sub.save()
    return redirect('products')