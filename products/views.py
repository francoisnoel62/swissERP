from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from .forms import ProductModelForm
from .models import Product


class ProductListView(generic.ListView):
    template_name = 'product/products_listview.html'
    context_object_name = 'products_list'
    model = Product


class ProductCreateView(generic.CreateView):
    template_name = 'product/create_product.html'
    form_class = ProductModelForm


class ProductUpdateView(generic.UpdateView):
    template_name = 'product/create_product.html'
    form_class = ProductModelForm
    model = Product


class ProductDeleteView(generic.DeleteView):
    model = Product
    success_url = reverse_lazy("products")

    def delete(self, request, *args, **kwargs):
        deleted_product = super(ProductDeleteView, self).get_object()
        messages.success(self.request, f"{deleted_product.name} was removed from DB  ")
        return super(ProductDeleteView, self).delete(request, *args, **kwargs)
