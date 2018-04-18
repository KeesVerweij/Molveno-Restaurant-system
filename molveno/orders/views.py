from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin, auth, messages
from .models import *
from django.forms import ModelForm
# Create your views here.


def order_history_view(request):
    orderhist = [item.menu_item for item in Order.objects.filter(completed=True)]       #if item.completed('True')
    print('Orderhistory: ', orderhist)
    return render(request,'restaurant/order_history.html',{'orderhist': orderhist})
