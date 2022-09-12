from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
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
            )
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

    def delete(self, request, *args, **kwargs):
        deleted_product = super(ProductDeleteView, self).get_object()
        messages.success(self.request, f"{deleted_product.name} was removed from DB  ")
        return super(ProductDeleteView, self).delete(request, *args, **kwargs)
