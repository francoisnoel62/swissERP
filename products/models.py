from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name="Nom de la catégorie", max_length=50)
    categ_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


class Product(models.Model):
    name = models.CharField(verbose_name="Nom du produit", max_length=50)
    price = models.FloatField(verbose_name="Prix du produit")
    description = models.TextField(verbose_name="Description du produit", null=True)
    picture = models.ImageField(verbose_name="Illustrations", upload_to='products', null=True)
    categ_id = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True)
    tax_ids = models.ManyToManyField("tax.AccountTax")

    def __str__(self):
        return self.name
