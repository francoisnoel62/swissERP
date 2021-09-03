from django import forms
from .models import ContactsImport


class ImportContactsModelForm(forms.ModelForm):
    class Meta:
        model = ContactsImport
        fields = '__all__'
