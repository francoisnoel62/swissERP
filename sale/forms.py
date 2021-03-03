from django import forms
from django.forms import SelectDateWidget

from .models import SaleOrder, SaleOrderLine


class SaleModelForm(forms.ModelForm):
    validity_date = forms.DateField(widget=SelectDateWidget())

    class Meta:
        model = SaleOrder
        fields = '__all__'


class SaleOrderLineForm(forms.ModelForm):
    class Meta:
        model = SaleOrderLine
        fields = '__all__'
        exclude = ['create_at', 'updated_at']
