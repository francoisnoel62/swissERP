import csv

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from swissERP.settings import AUTH_USER_MODEL


class ContactsImport(models.Model):
    file = models.FileField(upload_to="contacts")


class Contact(models.Model):
    TITLE_CHOICES = (
        ('Mr', 'Mister'),
        ('Ms', 'Madame'),
        ('Miss', 'Miss'),
    )

    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="active", default=True)
    title = models.CharField(verbose_name="titre", max_length=50, choices=TITLE_CHOICES, default='Mme')
    name = models.CharField(verbose_name='Prénom', max_length=200)
    lastname = models.CharField(verbose_name='Nom de famille', max_length=200)
    email = models.EmailField(verbose_name="E-mail", max_length=254)
    phone = PhoneNumberField(null=True)
    date_of_birth = models.DateField("Date of birth")
    street = models.CharField(verbose_name="Adresse", max_length=100)
    region_zip = models.CharField(verbose_name="Code postale", max_length=50)
    city = models.CharField(verbose_name="Ville", max_length=60)
    country = models.CharField(verbose_name="Pays", max_length=50)

    def get_absolute_url(self):
        return reverse('contact_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.name} {self.lastname}"

    @staticmethod
    def process_data(file, current_user):
        if file and current_user:
            doc = ContactsImport.objects.get(pk=file.id)
            with open(doc.file.path) as f:
                reader = csv.reader(f, delimiter=";")
                next(reader, None)
                for row in reader:
                    _, created = Contact.objects.get_or_create(
                        is_active=row[0],
                        title=row[1],
                        lastname=row[2],
                        name=row[3],
                        date_of_birth=row[4],
                        street=row[5],
                        region_zip=row[6],
                        city=row[7],
                        country=row[8],
                        phone=row[9],
                        email=row[10],
                        user_id=current_user
                    )
