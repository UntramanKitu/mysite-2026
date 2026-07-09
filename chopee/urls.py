from django.urls import path
from . import views

app_name = 'chopee'

urlpatterns = [
    path('', views.products_list, name='products_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('shops/', views.shops_list, name='shops_list'),
    path('shop/<int:pk>/', views.shop_detail, name='shop_detail'),
    path('profile/', views.user_profile, name='user_profile'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
]
