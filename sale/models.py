from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from contacts.models import Contact
from products.models import Product


class SaleOrder(models.Model):
    ORDER_STATE = (
        ('DR', 'Draft'),
        ('PG', 'Pending'),
        ('CF', 'Confirmed'),
        ('CC', 'Canceled')
    )

    create_at = models.DateTimeField(auto_now_add=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    partner_id = models.ForeignKey(Contact, on_delete=models.CASCADE, null=False, verbose_name='Customer')
    validity_date = models.DateField(verbose_name="Validity date", blank=True, null=True)
    order_state = models.CharField(verbose_name="Etat de la commande", max_length=10, choices=ORDER_STATE, default='DR')

    @property
    def state_color(self):
        if self.order_state == 'DR':
            return "badge-info"
        elif self.order_state == 'PG':
            return "badge-secondary"
        elif self.order_state == 'CF':
            return "badge-warning"
        elif self.order_state == 'CC':
            return "badge-danger"

    @property
    def total(self):
        res = False
        for sol in self.saleorderline_set.all():
            res += sol.sol_total
        return round(res, 2)

    def get_absolute_url(self):
        return reverse('sale_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.name}"


class SaleOrderLine(models.Model):
    create_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, verbose_name="Products")
    quantity = models.FloatField(default=1, verbose_name="Quantity")
    sol_total = models.FloatField(verbose_name="Total", max_length=100)
    sale_order_id = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.product_id.name} - {self.quantity} - {self.sol_total}"
