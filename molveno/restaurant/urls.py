from django.urls import path
from . import views

app_name = 'restaurant'
urlpatterns = [
    path('inventory/',views.InventoryPageView.as_view(),name="inventory"),
]
