from django import forms
from django.forms import widgets

from .models import Product, Subscription, UnitPass


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['created_by']


class PassModelForm(forms.ModelForm):
    class Meta:
        model = UnitPass
        fields = '__all__'
        exclude = ['created_by']
        widgets = {
            'date_of_buy': widgets.DateInput(attrs={'type': 'date'}),
        }


class SubModelForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = '__all__'
        exclude = ['created_by']
        widgets = {
            'date_of_subscription': widgets.DateInput(attrs={'type': 'date'}),
        }

