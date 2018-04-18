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
            amount = orders[item]
            item_id = MenuItem.objects.values().filter(name=item)[0]['id']
            item_price = MenuItemAddition.objects.values().filter(menu_item=item_id)[
                0]['selling_price']
            order_price = item_price * amount
            print(order_price)
            self.fields[item] = forms.CharField(help_text=str(order_price), label_suffix='', widget=TextInput(attrs={
                'min': '1', 'max': '10', 'type': 'number', 'value': orders[item]}))
