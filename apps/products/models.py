from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from swissERP.settings import AUTH_USER_MODEL


class Product(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(verbose_name="Nom du produit", max_length=50)
    price = models.FloatField(verbose_name="Prix du produit")
    description = models.TextField(verbose_name="Description du produit", null=True)
    picture = models.ImageField(verbose_name="Illustrations", upload_to='images', null=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products')

    @property
    def state_color(self):
        if not self.finished:
            return "badge-info"
        else:
            return "badge-danger"
