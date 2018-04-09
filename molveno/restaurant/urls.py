from django.urls import path
from . import views

app_name = 'restaurant'
urlpatterns = [
    path('restaurant/',views.IndexView.as_view(),name="index"),
    path('inventory/',views.InventoryPageView.as_view(), name = "inventory"),
    path('restaurant/Menu/', views.MenuChangeView.as_view(), name = "menu-change-view"),
    path('restaurant/Menu/add/', views.MenuAddView.as_view(), name = "menu-add-view"),
    path('restaurant/Supplier/', views.SupplierChangeView.as_view(), name = "supplier-change-view"),
    path('restaurant/Supplier/add/', views.SupplierAddView.as_view(), name = "supplier-add-view"),
    path('menuitem/<int:pk>/', views.MenuItemView.as_view(), name="menu_item"),
    path('addorder/<int:item_id>/', views.AddOrderView, name="addorder"),
    path('MenuCard/<int:table_id>/', views.MenuCardList.as_view(), name="MenuCard")
]
