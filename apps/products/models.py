from datetime import timedelta, datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from model_utils.managers import InheritanceManager

from apps.contacts.models import Contact
from swissERP.settings import AUTH_USER_MODEL


class Product(models.Model):
    objects = InheritanceManager()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Nom du produit", max_length=50)
    student = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="products", verbose_name="Élève",
                                null=True, blank=True, limit_choices_to={'is_active': True})

    def __str__(self):
        return f"{self.name} - {self.student}"

    def get_absolute_url(self):
        return reverse('products')


class Subscription(Product):
    classes_by_week = models.IntegerField(verbose_name="Nombre de cours par semaine", default=1)
    date_of_subscription = models.DateField(verbose_name="Date d'abonnement")
    recurrence = models.CharField(verbose_name="Récurrence", choices=[("M", "Mensuel"), ("A", "Annuel")],
                                  max_length=100)
    current_credits = models.IntegerField(verbose_name="Crédits restants")

    @property
    def date_of_renewal(self):
        if self.recurrence == "M":
            return datetime.strptime(self.date_of_subscription, "%Y-%m-%d") + timedelta(days=31)
        else:
            return datetime.strptime(self.date_of_subscription, "%Y-%m-%d") + relativedelta(years=1)


class UnitPass(Product):
    remaining_classes = models.IntegerField(verbose_name="Nombre de cours restants", default=10)
    date_of_buy = models.DateField(verbose_name="Date d'achat")

    @property
    def end_of_validity(self):
        return datetime.strptime(self.date_of_buy, "%Y-%m-%d") + relativedelta(years=1)
