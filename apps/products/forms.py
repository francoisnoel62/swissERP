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

    def save(self, commit=True):
        temp = super(PassModelForm, self).save(commit=True)
        temp.name = temp.name + " // " + str(temp.student)
        if commit:
            temp.save()
        return temp


class SubModelForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = '__all__'
        exclude = ['created_by']

    def save(self, commit=True):
        temp = super(SubModelForm, self).save(commit=True)
        temp.name = temp.name + " // " + str(temp.student)
        if commit:
            temp.save()
        return temp
