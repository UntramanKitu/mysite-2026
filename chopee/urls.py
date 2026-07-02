from django.urls import path
from . import views

app_name = 'chopee'

urlpatterns = [
    path('', views.products_list, name='products_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('shops/', views.shops_list, name='shops_list'),
]
