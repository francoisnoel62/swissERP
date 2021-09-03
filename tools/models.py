from django.db import models


class ContactsImport(models.Model):
    title = models.CharField(verbose_name="file name", max_length=50, null=True)
    file = models.FileField(upload_to="contacts")
