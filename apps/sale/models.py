from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from apps.base_model import BaseModel
from apps.contacts.models import Contact
from apps.products.models import Product


class SaleOrder(BaseModel):
    ORDER_STATE = (
        ('DR', 'Draft'),
        ('CL', 'Cleaned'),
        ('CF', 'Confirmed'),
        ('SD', 'Send'),
        ('PD', 'Paid'),
    )

    name = models.CharField(max_length=100)
    partner_id = models.ForeignKey(Contact, on_delete=models.PROTECT, null=False, verbose_name='Customer',
                                   limit_choices_to={'is_active': True})
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
        elif self.order_state == 'PD':
            return "badge-success"

    @property
    def total(self):
        res = False
        for sol in self.saleorderline_set.all():
            res += sol.sol_total
        return round(res, 2)

    @property
    def solde(self):
        total_payment = False
        for payment in self.payment_set.all():
            total_payment += payment.total
        return round(self.total - total_payment)

    def get_absolute_url(self):
        return reverse('sale_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.name}"


class SaleOrderLine(BaseModel):
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT, null=False, verbose_name="Products")
    quantity = models.FloatField(default=1, verbose_name="Quantity")
    sol_total = models.FloatField(verbose_name="Total", max_length=100)
    sale_order_id = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.product_id.name} - {self.quantity} - {self.sol_total}"

    def save(self, *args, **kwargs):
        existing_sol = self.__class__.objects.filter(product_id=self.product_id,
                                                     sale_order_id=self.sale_order_id).first()
        if existing_sol:
            self.quantity += existing_sol.quantity
            existing_sol.delete()
        super(SaleOrderLine, self).save(*args, **kwargs)


class SomeModel(BaseModel):
    pass
