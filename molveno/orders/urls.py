from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('order_history/',views.OrderHistoryView.as_view(), name = 'order_history'),
]
