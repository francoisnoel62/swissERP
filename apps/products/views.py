from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import ProductModelForm
from .models import Product


class ProductListView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('login')
    template_name = 'product/products_listview.html'
    context_object_name = 'products_list'

    def get_queryset(self):
        query = self.request.GET.get("filter")
        if query:
            object_list = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            ).filter(created_by=self.request.user)
            return object_list
        return Product.objects.filter(created_by=self.request.user)


class ProductCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'product/create_product.html'
    form_class = ProductModelForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'product/create_product.html'
    form_class = ProductModelForm
    model = Product


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
