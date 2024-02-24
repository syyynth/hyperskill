from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'name', 'surname', 'phone_number'
        labels = {
            'name': 'your name',
            'surname': 'your surname',
            'phone_number': 'your phone number',
        }
