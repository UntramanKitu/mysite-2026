from django.urls import path
from . import views

app_name = 'chopee'

urlpatterns = [
    # สินค้า
    path('', views.products_list, name='products_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # ร้านค้า
    path('shops/', views.shops_list, name='shops_list'),
    path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    
    # ตะกร้า
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # คำสั่งซื้อ
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders_list, name='orders_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # รีวิว
    path('product/<int:product_id>/review/', views.add_review, name='add_review'),
    
    # โปรไฟล์
    path('profile/', views.user_profile, name='user_profile'),
]
