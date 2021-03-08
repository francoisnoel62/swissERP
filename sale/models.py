from django.db import models
from django.urls import reverse

from contacts.models import Contact
from products.models import Product


class SaleOrder(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    partner_id = models.ForeignKey(Contact, on_delete=models.CASCADE, null=False, verbose_name='Customer')
    validity_date = models.DateField(verbose_name="Validity date", blank=True, null=True)
    so_total = models.CharField(verbose_name="Total", max_length=100, blank=True)

    def get_absolute_url(self):
        return reverse('sale_detail', kwargs={'pk': self.pk})


class SaleOrderLine(models.Model):
    create_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, verbose_name="Products")
    quantity = models.FloatField(default=1, verbose_name="Quantity")
    sol_total = models.FloatField(verbose_name="Total", max_length=100)
    sale_order_id = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)
