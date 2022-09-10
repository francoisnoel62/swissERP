from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.utils import timezone

from apps.sale.models import SaleOrder


class Payment(models.Model):
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

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    currency = models.CharField(verbose_name="Monnaie", max_length=50, choices=CURRENCIES, default='CHF')
    total = models.FloatField(verbose_name="Montant")
    payment_method = models.CharField(verbose_name="Payment method", max_length=50, choices=PAYMENT_METHOD, default='IBAN')
    date = models.DateField(verbose_name="Date du paiement", default=timezone.now)
    sale_id = models.OneToOneField(SaleOrder, on_delete=models.CASCADE)
