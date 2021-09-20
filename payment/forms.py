from django import forms

from payment.models import Payment


class PaymentForm(forms.ModelForm):
    def __init__(self):
        super(PaymentForm, self).__init__()
        self.fields['total'].disabled = True
        self.fields['date'].disabled = True
        self.fields['invoice_id'].disabled = True

    class Meta:
        model = Payment
        exclude = ['create_at', 'updated_at', 'created_by']
        fields = '__all__'

