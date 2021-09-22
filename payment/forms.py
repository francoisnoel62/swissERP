import datetime

from django import forms

from payment.models import Payment


class PaymentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        initial=datetime.datetime.now()
    )

    class Meta:
        model = Payment
        exclude = ['create_at', 'updated_at']
        fields = '__all__'

