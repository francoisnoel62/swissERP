from django import forms
from django.core.exceptions import ValidationError

from .models import Contact
from .models import ContactsImport


class ContactsModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ['is_active', 'user_id']


class ImportContactsModelForm(forms.ModelForm):
    class Meta:
        model = ContactsImport
        fields = '__all__'

    def clean(self):
        file_path = str(self.cleaned_data.get('file'))
        if not file_path.endswith(".csv"):
            raise ValidationError('Please use CSV file !')
        return self.cleaned_data
