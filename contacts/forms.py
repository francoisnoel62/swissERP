from django import forms
from .models import Contact


class ContactsModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
