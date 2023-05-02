from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from apps.base_model import BaseModel
from apps.sale.models import SaleOrder


class Payment(BaseModel):
    CURRENCIES = (
        ('CHF', 'Francs Suisse'),
        ('EU', 'Euros'),
    )

    PAYMENT_METHOD = (
        ('IBAN', 'Virement bancaire'),
        ('TW', 'Twint'),
        ('CS', 'Cash'),
        ('CB', 'Carte de crédit'),
    )

    currency = models.CharField(verbose_name="Monnaie", max_length=50, choices=CURRENCIES, default='CHF')
    total = models.FloatField(verbose_name="Montant")
    payment_method = models.CharField(verbose_name="Payment method", max_length=50, choices=PAYMENT_METHOD, default='IBAN')
    date = models.DateField(verbose_name="Date du paiement", default=timezone.now)
    sale_id = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)

    def __str__(self):
        return f"facture:{self.sale_id.name} // Date de paiement:{self.date}"

    def save(self, *args, **kwargs):
        if self.total > self.sale_id.solde:
            raise Exception("Payment value is superior to invoice total")
        return super(Payment, self).save(*args, **kwargs)


