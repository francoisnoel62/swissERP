from django import forms
from django.forms import inlineformset_factory, widgets

from .models import Presence, Session


class SessionsModelForm(forms.ModelForm):
    class Meta:
        model = Session
        exclude = ['create_at', 'updated_at', 'created_by']
        widgets = {
            'date': widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class PresenceModelForm(forms.ModelForm):
    class Meta:
        model = Presence
        exclude = ['create_at', 'updated_at']
        widgets = {
            'comment': widgets.Textarea(attrs={'rows': 1, 'cols': 20})
        }


PresenceFormSet = inlineformset_factory(Session, Presence, form=PresenceModelForm, extra=1)
