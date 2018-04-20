from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin, auth, messages
from restaurant.models import *
from django.forms import ModelForm
from datetime import datetime, timedelta


class IndexView(TemplateView):
    template_name = "orders/index.html"


class OrderHistoryView(generic.ListView):
    template_name = 'orders/order_history.html'
    context_object_name = 'complete_order_list'

    def get_queryset(self):
        return Order.objects.all().filter(completed=True)


class FoodOrdersList(TemplateView):
    template_name = 'orders/foodorders.html'

    def get_current_orders(self):
        current_orders = Order.objects.filter(completed=False)
        return current_orders

    def get_food_orders(self):
        current_orders = self.get_current_orders()
        food_orders = [i for i in current_orders if str(i.menu_item.course_type) != 'Drink']
        food_orders = sorted(food_orders, key=lambda order: order.order_time, reverse=False)
        for i in food_orders:
            displayed_time = i.order_time + timedelta(hours=2)
            i.order_time = format(displayed_time, '%H:%M')
        return food_orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['food_orders'] = self.get_food_orders()
        return context

class DrinkOrdersList(TemplateView):
    template_name = 'orders/drinkorders.html'

    def get_current_orders(self):
        current_orders = Order.objects.filter(completed=False)
        return current_orders

    def get_drink_orders(self):
        current_orders = self.get_current_orders()
        drink_orders = [i for i in current_orders if str(i.menu_item.course_type) == 'Drink']
        drink_orders = sorted(drink_orders, key=lambda order: order.order_time, reverse=False)
        for i in drink_orders:
            displayed_time = i.order_time + timedelta(hours=2)
            i.order_time = format(displayed_time, '%H:%M')
        return drink_orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drink_orders'] = self.get_drink_orders()
        return context

class OrderRecipe(TemplateView):
    template_name = 'orders/orderrecipe.html'

    def get_ingredients(self):
        recipe_ingredients = Ingredient.objects.filter(menu_item__in=MenuItem.objects.filter(id = self.kwargs['pk']))
        return recipe_ingredients

    def get_recipe(self):
        recipe = Order.objects.filter(menu_item__in=MenuItem.objects.filter(id = self.kwargs['pk']))
        return recipe[0].menu_item.recipe

    def get_menu_item(self):
        orders = Order.objects.filter(menu_item__in=MenuItem.objects.filter(id = self.kwargs['pk']))
        return orders[0].menu_item.name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.get_recipe()
        context['menuitem'] = self.get_menu_item()
        context['ingredients'] = self.get_ingredients()
        return context
