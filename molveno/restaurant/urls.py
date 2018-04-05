from django.urls import path
from . import views

app_name = 'restaurant'
urlpatterns = [
    path('inventory/', views.InventoryPageView.as_view(), name="inventory"),
    path('menuitem/<int:pk>/', views.MenuItemView.as_view(), name="menu_item"),
    path('addorder/<int:item_id>/', views.AddOrderView, name="addorder"),
]
