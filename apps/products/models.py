from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
from django.urls import reverse


class Product(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(verbose_name="Nom du produit", max_length=50)
    price = models.FloatField(verbose_name="Prix du produit")
    description = models.TextField(verbose_name="Description du produit", null=True)
    picture = models.ImageField(verbose_name="Illustrations", upload_to='images')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    finished = models.BooleanField("Etat", default=True, null=False)

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
