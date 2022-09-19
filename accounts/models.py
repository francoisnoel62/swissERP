from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    street = models.CharField(max_length=100)
    zip = models.IntegerField(verbose_name="zip code")
    city = models.CharField(max_length=55)
    telephone = PhoneNumberField(null=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('home')
