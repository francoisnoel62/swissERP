from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from bankAccount.models import BankAccount


class Company(models.Model):
    name = models.CharField(verbose_name='Nom Entreprise', max_length=100)
    street = models.CharField(verbose_name="Adresse", max_length=100)
    region_zip = models.IntegerField(verbose_name="Code postale", null=True)
    city = models.CharField(verbose_name="Ville", max_length=200, null=True)
    state = models.CharField(verbose_name="Etat", max_length=100)
    country = models.CharField(verbose_name="Pays", max_length=100)
    phone = PhoneNumberField()
    email = models.EmailField(verbose_name="E-mail", max_length=100)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
