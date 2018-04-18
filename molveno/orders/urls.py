from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('order_history',views.order_history_view, name = 'order_history'),
]
