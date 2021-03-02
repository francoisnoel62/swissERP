from django import forms
from django.forms import SelectDateWidget

from .models import SaleOrder


class SaleModelForm(forms.ModelForm):
    validity_date = forms.DateField(widget=SelectDateWidget())

    class Meta:
        model = SaleOrder
        fields = '__all__'
