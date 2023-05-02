from django.db import models
from django.urls import reverse

from apps.base_model import BaseModel
from apps.contacts.models import Contact
from apps.products.models import Product


class Session(BaseModel):
    name = models.CharField(verbose_name="Classe name", max_length=50)
    date = models.DateTimeField(verbose_name="Date et heure")
    terminated = models.BooleanField(verbose_name="Terminated", default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sessions')


class Presence(BaseModel):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Contact, on_delete=models.CASCADE, null=False, verbose_name='Student',
                                 limit_choices_to={'is_active': True})
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, verbose_name='Product')
    comment = models.TextField(verbose_name="Comments", blank=True, null=True)

    def __str__(self):
        return self.session_id.name + " - " + self.attendee.name + " - " + self.product.name
