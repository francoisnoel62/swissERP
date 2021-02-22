from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    title = models.CharField(verbose_name="titre", max_length=50, null=True)
    lang = models.CharField(verbose_name="Langue", max_length=80, null=True, blank=True)
    name = models.CharField(verbose_name='Prénom', max_length=200, null=True)
    lastname = models.CharField(verbose_name='Nom de famille', max_length=200, null=True)
    age = models.IntegerField(verbose_name='Age', null=True)
    street = models.CharField(verbose_name="Addresse", max_length=100, null=True)
    region_zip = models.IntegerField(verbose_name="Code postale", null=True)
    city = models.CharField(verbose_name="Ville", max_length=200, null=True)
    country = models.CharField(verbose_name="Pays", max_length=100, null=True)
    phone = PhoneNumberField(null=True)
    mobile = PhoneNumberField(null=True)
    email = models.EmailField(verbose_name="E-mail", max_length=254, null=True)
    state = models.CharField(verbose_name="Etat", max_length=20, null=True)

    def get_absolute_url(self):
        return reverse('contact_detail', kwargs={'pk': self.pk})
