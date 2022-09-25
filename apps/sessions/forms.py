from django import forms
from django.forms import Form, ModelForm, DateField, widgets

from .models import Session


class SessionsModelForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = '__all__'
        exclude = ['user_id']
        widgets = {
            'date': widgets.DateInput(attrs={'type': 'date'}),
            'schedule': widgets.DateTimeInput(attrs={'type': 'time'}),
            'attendees': widgets.CheckboxSelectMultiple()
        }
