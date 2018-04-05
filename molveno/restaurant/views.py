from django.shortcuts import render
from django.views.generic.base import TemplateView

from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered

from django.contrib import admin, auth

from .models import *

from django.forms import ModelForm



# We will use class-based views
# TemplateView is a class that renders an html page with django variables in double curly brackets {{ }}

class InventoryPageView(TemplateView):

    # this is a reserved variable that leads to the html template page.
    template_name = "restaurant/inventory.html"

class IndexView(TemplateView):
    template_name = "restaurant/index.html"

    # get overview of all models in our app
    restaurant_app = apps.get_app_config('restaurant')
    restaurant_app_models = restaurant_app.models.values()
    restaurant_app_model_names = [model._meta.verbose_name for model in restaurant_app_models]

    # comes out e.g. as 'restaurant.menu_menu_items'
    model_short_names = [model._meta.label_lower for model in restaurant_app_models]

    # admin.site._registry is a dictionary with all registered tables
    registered_model_names = [key._meta.verbose_name.capitalize() for key in admin.site._registry]

    # replace the dot after the app prefix with a slash, for the url
    model_short_names_as_links = ['management/'+short_name.replace('restaurant.', 'restaurant/') + '/' for short_name in model_short_names]


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models'] = self.registered_model_names
        context['links'] = self.model_short_names_as_links
        context['title'] = 'Site Administration'
        context['table_title'] = 'Restaurant'

        return context

class MenuAddView(TemplateView):
    template_name = "restaurant/menu-add.html"

    # query to get all items out of menu table
    menu_table = Menu.objects.all()
    print(menu_table)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = self.menu_table
        return context

class MenuChangeView(TemplateView):
    template_name = "restaurant/menu-change.html"
    menu_table = Menu.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = self.menu_table
        return context

class SupplierAddView(TemplateView):
    template_name = "restaurant/supplier-add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class SupplierChangeView(TemplateView):
    template_name = "restaurant/supplier-change.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
