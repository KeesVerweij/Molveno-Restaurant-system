from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.forms.widgets import TextInput


class MenuItemForm(forms.Form):
    order_amount = forms.CharField(widget=TextInput(attrs={
        'min': '1', 'max': '10', 'type': 'number', 'placeholder': '1'}))


class OrderForm(forms.Form):
    def __init__(self, orders, validate, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        if validate:
            print('validate form')
            for key in orders:
                self.fields[key] = forms.CharField(widget=TextInput(attrs={
                    'min': '1', 'max': '10', 'type': 'number'}))
        else:
            print('create form')
            for key in orders:
                self.fields[key] = forms.CharField(widget=TextInput(attrs={
                    'min': '1', 'max': '10', 'type': 'number', 'value': orders[key]}))
