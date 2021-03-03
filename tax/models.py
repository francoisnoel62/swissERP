from django.db import models


# Create your models here.

class AccountTax(models.Model):
    name = models.CharField(verbose_name="Nom de la taxe", max_length=50)
    amount = models.FloatField(verbose_name="Valeur de la taxe")

    def __str__(self):
        return self.name