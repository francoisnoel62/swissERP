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