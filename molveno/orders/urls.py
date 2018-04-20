from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('order_history/',views.OrderHistoryView.as_view(), name = 'order_history'),
    path('main', views.IndexView.as_view(), name = 'index'),
    path('food_orders/', views.FoodOrdersList.as_view(), name = 'food_orders'),
    path('drink_orders/', views.DrinkOrdersList.as_view(), name = 'drink_orders'),
    path('orders/recipe/<int:pk>/', views.OrderRecipe.as_view(), name='recipe'),
]
