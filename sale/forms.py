import datetime

from django import forms
from django.forms import inlineformset_factory

from .models import SaleOrder, SaleOrderLine


class SaleModelForm(forms.ModelForm):
    validity_date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'},
        ),
    )

    class Meta:
        model = SaleOrder
        exclude = ['name', 'order_state', 'created_by']

    def save(self, commit=True):
        temp = super(SaleModelForm, self).save(commit=True)
        date = temp.validity_date.strftime("%d-%m-%Y")
        temp.name = f"Order#{temp.id} - {temp.partner_id.name} {temp.partner_id.lastname} - {date} - {temp.total}CHF"
        if commit:
            temp.save()
        return temp


class SaleOrderLineModelForm(forms.ModelForm):
    class Meta:
        model = SaleOrderLine
        exclude = ['sol_total']

    def save(self, commit=True):
        temp = super(SaleOrderLineModelForm, self).save(commit=False)
        temp.sol_total = temp.product_id.price * temp.quantity
        if commit:
            temp.save()
        return temp


SaleOrderLineFormSet = inlineformset_factory(SaleOrder, SaleOrderLine, form=SaleOrderLineModelForm, extra=2)
