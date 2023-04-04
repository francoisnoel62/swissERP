from django.db import models
from django.urls import reverse

from apps.contacts.models import Contact
from swissERP.settings import AUTH_USER_MODEL


# Create your models here.
class Session(models.Model):
    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Classe name", max_length=50)
    date = models.DateField(verbose_name="Date")
    attendees = models.ManyToManyField(Contact, related_name="sessions", limit_choices_to={'is_active': True})
    terminated = models.BooleanField(verbose_name="Terminated", default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sessions')

