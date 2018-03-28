from django.shortcuts import render
from django.views.generic.base import TemplateView

# We will use class-based views
# TemplateView is a class that renders an html page with django variables in double curly brackets {{ }}

class InventoryPageView(TemplateView):

    # this is a reserved variable that leads to the html template page.
    template_name = "restaurant/inventory.html"
