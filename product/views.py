from django.views import generic
from .models import Product

class IndexView(generic.ListView):
    template_name = 'product/products_listview.html'
    context_object_name = 'products_list'

    def get_queryset(self):
        return Product.objects.all()