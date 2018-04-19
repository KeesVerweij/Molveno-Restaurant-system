from django import forms
from .models import MenuItem, MenuItemAddition
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms.widgets import TextInput


class MenuItemForm(forms.Form):
    order_amount = forms.CharField(widget=TextInput(attrs={
        'min': '1', 'max': '10', 'type': 'number', 'placeholder': '1'}))


class OrderForm(forms.Form):
    def __init__(self, orders, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for item in orders:
            amount = orders[item]['amount']
            price = orders[item]['price']
            self.fields[item] = forms.CharField(
                help_text=str(price),
                label_suffix='',
                widget=TextInput(attrs={
                    'min': '1', 'max': '10', 'type': 'number', 'value': amount
                }))
