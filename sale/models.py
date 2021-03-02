from django.db import models
from django.urls import reverse

from contacts.models import Contact
from products.models import Product


class SaleOrder(models.Model):
    # create_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    partner_id = models.ForeignKey(Contact, on_delete=models.CASCADE, null=False, verbose_name='Customer')
    validity_date = models.DateField(verbose_name="Validity date", blank=True, null=True)
    so_total = models.CharField(verbose_name="Total", max_length=100)

    def get_absolute_url(self):
        return reverse('sales')

    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #
    #     for sol in self.saleorderline_set.all():
    #         self.so_total += sol.sol_total
    #
    #     return super(SaleOrder, self).save(self, force_insert=False, force_update=False, using=None, update_fields=None)


class SaleOrderLine(models.Model):
    create_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, verbose_name="Products")
    quantity = models.FloatField(default=1, verbose_name="Quantity")
    ht_price = models.FloatField(verbose_name="HT price")
    tax_id = models.ManyToManyField("tax.AccountTax", verbose_name="Tax")
    sol_total = models.FloatField(verbose_name="Total", max_length=100)
    sale_order_id = models.ForeignKey(SaleOrder, on_delete=models.CASCADE, null=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.ht_price = self.product_id.price * self.quantity

        if self.product_id.tax_ids:
            self.tax_id = self.product_id.tax_ids[0]
            if self.tax_id:
                self.sol_total = self.ht_price + ((self.ht_price * self.tax_id.amount) / 100)
        else:
            self.sol_total = self.ht_price

        return super(SaleOrderLine, self).save(self, force_insert=False, force_update=False, using=None, update_fields=None)
