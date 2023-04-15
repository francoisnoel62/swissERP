from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from apps.contacts.models import Contact
from swissERP.settings import AUTH_USER_MODEL


class Product(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Nom du produit", max_length=50)
    price = models.FloatField(verbose_name="Prix du produit")
    student = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="products", verbose_name="Élève",
                                null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products')


class Subscription(Product):
    classes_by_month = models.IntegerField(verbose_name="Nombre de cours par mois")


class UnitPass(Product):
    remaining_classes = models.IntegerField(verbose_name="Nombre de cours restants", default=10)
