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


class OrderHistoryView(generic.ListView):
    template_name = 'orders/order_history.html'
    context_object_name = 'complete_order_list'

    def get_queryset(self):
        return Order.objects.all().filter(completed=True)
