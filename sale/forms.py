from django import forms
from django.forms import SelectDateWidget

from .models import SaleOrder, SaleOrderLine


class SaleModelForm(forms.ModelForm):
    validity_date = forms.DateField()

    class Meta:
        model = SaleOrder
        fields = '__all__'
        # exclude = ['name']

    def save(self, commit=True):
        temp = super(SaleModelForm, self).save(commit=True)
        date = temp.validity_date.strftime("%d-%m-%Y")
        temp.name = f"Order#{temp.id} - {temp.partner_id.name} {temp.partner_id.lastname} - {date} - {temp.so_total}CHF"
        if commit:
            temp.save()
        return temp

