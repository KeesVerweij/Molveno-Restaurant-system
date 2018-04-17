from django.urls import path
from . import views

app_name = 'restaurant'
urlpatterns = [
    path('restaurant/', views.IndexView.as_view(), name="index"),
    path('inventory/', views.InventoryPageView.as_view(), name="inventory"),
    path('restaurant/menu/', views.MenuChangeView.as_view(), name="menu-change-view"),
    path('restaurant/menu/add/', views.MenuAddView.as_view(), name="menu-add-view"),
    path('restaurant/supplier/', views.SupplierChangeView.as_view(), name="supplier-change-view"),
    path('restaurant/supplier/add/', views.SupplierAddView.as_view(), name="supplier-add-view"),
    path('menuitem/<int:pk>/', views.MenuItemView.as_view(), name="menu_item"),
    path('addorder/<int:item_id>/', views.add_order_view, name="addorder"),
    path('orders/', views.orders_view, name="orders"),
    path('menucard/<int:table_id>/', views.MenuCardList.as_view(), name="menucard"),
    path('waiter/', views.request_waiter, name="waiter"),
]
