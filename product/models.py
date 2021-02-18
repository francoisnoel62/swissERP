from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(verbose_name="Nom du produit", max_length=50)
    price = models.FloatField(verbose_name="Prix du produit")
    description = models.TextField(verbose_name="Description du produit", null=True)
    picture = models.ImageField(verbose_name="Illustrations", upload_to='product', null=True)