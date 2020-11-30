from django.db import models


class Contact(models.Model):
    name = models.CharField(verbose_name='Nom du contact', max_length=200)
    age = models.IntegerField(verbose_name='age')