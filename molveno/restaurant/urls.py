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
]
