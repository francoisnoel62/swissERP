from django.db import models


class BankAccount(models.Model):
    bank_name = models.CharField(verbose_name='Nom Banque', max_length=100)
    iban = models.IntegerField(verbose_name='IBAN')
    recipient = models.CharField(verbose_name='Recipient', max_length=100)
