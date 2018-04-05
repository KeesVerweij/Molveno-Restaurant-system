from django import forms
from django.forms.widgets import TextInput


class AddOrderForm(forms.Form):
    order_amount = forms.CharField(widget=TextInput(attrs={
        'min': '1', 'max': '5', 'type': 'number', 'placeholder': '1'}))
