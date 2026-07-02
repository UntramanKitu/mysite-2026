from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.files.base import ContentFile
from django.utils.text import slugify
from decimal import Decimal
import uuid

from .models import (
    Product, Shop, Category, Cart, CartItem, 
    Order, OrderItem, Review, UserProfile
)

def seed_mock_products():
    """สร้างข้อมูลตัวอย่าง 5 สินค้าเพื่อให้หน้าแสดงผลเหมือน Shopeeทันที"""
    if Product.objects.exists():
        return

    seller, _ = User.objects.get_or_create(
        username='mock-seller',
        defaults={'is_active': True, 'is_staff': True}
    )
    shop, _ = Shop.objects.get_or_create(
        owner=seller,
        defaults={
            'shop_name': 'Mock Shop',
            'description': 'ร้านค้าตัวอย่างสำหรับแสดงผลสินค้า',
        },
    )

    categories_data = [
        ('Điện tử', 'electronics', 'สินค้ากลุ่มอุปกรณ์และเทคโนโลยี'),
        ('Beauty', 'beauty', 'ผลิตภัณฑ์ดูแลผิวและความงาม'),
        ('บ้าน & แฟชั่น', 'home-fashion', 'ของใช้ในบ้านและแฟชั่น'),
    ]
    categories = {}
    for name, slug, description in categories_data:
        category, _ = Category.objects.get_or_create(
            name=name,
            defaults={'slug': slug, 'description': description},
        )
        categories[name] = category

    def make_svg(name, bg, text):
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">
            <rect width="800" height="800" fill="{bg}"/>
            <rect x="40" y="40" width="720" height="720" rx="36" fill="rgba(255,255,255,0.15)"/>
            <text x="400" y="360" font-family="Arial, sans-serif" font-size="54" font-weight="700" text-anchor="middle" fill="{text}">{name}</text>
            <text x="400" y="440" font-family="Arial, sans-serif" font-size="28" text-anchor="middle" fill="{text}">Shopee Style</text>
        </svg>'''
        return ContentFile(svg.encode('utf-8'), name=f'{slugify(name)}.svg')

    products_data = [
        {
            'name': 'iPhone 15', 'slug': 'iphone-15', 'description': 'ดีไซน์บางเบา ประสิทธิภาพแรง',
            'price': Decimal('29900'), 'discount_percentage': 15, 'stock': 12, 'rating': 4.8, 'sold_count': 1280,
            'category': categories['Điện tử'], 'bg': '#ff5f3d', 'text': '#ffffff',
        },
        {
            'name': 'Sữa rửa mặt', 'slug': 'sua-rua-mat', 'description': 'ทำความสะอาดล้ำลึกให้ผิวเรียบเนียน',
            'price': Decimal('320'), 'discount_percentage': 10, 'stock': 25, 'rating': 4.6, 'sold_count': 980,
            'category': categories['Beauty'], 'bg': '#ff9f43', 'text': '#fff8e1',
        },
        {
            'name': 'รองเท้า Nike Air', 'slug': 'nike-air', 'description': 'รองเท้ารองรับนุ่มสบายสำหรับทุกวัน',
            'price': Decimal('1890'), 'discount_percentage': 20, 'stock': 18, 'rating': 4.7, 'sold_count': 760,
            'category': categories['บ้าน & แฟชั่น'], 'bg': '#1e272e', 'text': '#ffffff',
        },
        {
            'name': 'แอร์พัดลม', 'slug': 'fan', 'description': 'พัดลมคอมPACT กินไฟต่ำและเย็นฉ่ำ',
            'price': Decimal('890'), 'discount_percentage': 12, 'stock': 30, 'rating': 4.4, 'sold_count': 540,
            'category': categories['บ้าน & แฟชั่น'], 'bg': '#3dc1d3', 'text': '#ffffff',
        },
        {
            'name': 'หูฟัง Bluetooth', 'slug': 'headphone', 'description': 'เสียงคมชัดและแบตอึดนาน',
            'price': Decimal('1290'), 'discount_percentage': 8, 'stock': 16, 'rating': 4.9, 'sold_count': 860,
            'category': categories['Điện tử'], 'bg': '#5f27cd', 'text': '#ffffff',
        },
    ]

    for item in products_data:
        Product.objects.create(
            shop=shop,
            category=item['category'],
            name=item['name'],
            slug=item['slug'],
            description=item['description'],
            price=item['price'],
            discount_percentage=item['discount_percentage'],
            stock=item['stock'],
            image=make_svg(item['name'], item['bg'], item['text']),
            rating=item['rating'],
            sold_count=item['sold_count'],
        )


def products_list(request):
    """แสดงรายการสินค้า"""
    seed_mock_products()
    products = Product.objects.all()
    categories = Category.objects.all()
    
    # ค้นหา
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # ตัวกรองตามหมวดหมู่
    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # เรียงลำดับ
    sort = request.GET.get('sort', '-created_at')
    products = products.order_by(sort)
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'chopee/products.html', context)

def product_detail(request, slug):
    """แสดงรายละเอียดสินค้า"""
    product = get_object_or_404(Product, slug=slug)
    product.view_count += 1
    product.save()
    
    reviews = product.reviews.all()
    similar_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:5]
    
    context = {
        'product': product,
        'reviews': reviews,
        'similar_products': similar_products,
    }
    return render(request, 'chopee/product_detail.html', context)

def shop_detail(request, shop_id):
    """แสดงรายละเอียดของร้านค้า"""
    shop = get_object_or_404(Shop, id=shop_id)
    products = shop.products.all()
    
    # ค้นหาสินค้าในร้าน
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    context = {
        'shop': shop,
        'products': products,
        'search_query': search_query,
    }
    return render(request, 'chopee/shop_detail.html', context)

@login_required
def cart_view(request):
    """แสดงตะกร้าสินค้า"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {'cart': cart}
    return render(request, 'chopee/cart.html', context)

@login_required
@require_POST
def add_to_cart(request, product_id):
    """เพิ่มสินค้าลงในตะกร้า"""
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    return redirect('chopee:cart')

@login_required
@require_POST
def update_cart_item(request, item_id):
    """อัปเดตจำนวนสินค้าในตะกร้า"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('chopee:cart')

@login_required
@require_POST
def remove_from_cart(request, item_id):
    """ลบสินค้าออกจากตะกร้า"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('chopee:cart')

@login_required
def checkout(request):
    """ชำระเงิน"""
    cart = get_object_or_404(Cart, user=request.user)
    
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address', '')
        phone_number = request.POST.get('phone_number', '')
        
        if not shipping_address or not phone_number:
            context = {'cart': cart, 'error': 'กรุณากรอกที่อยู่และเบอร์โทรศัพท์'}
            return render(request, 'chopee/checkout.html', context)
        
        # สร้างคำสั่งซื้อ
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        total_price = cart.total_price
        
        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            total_price=total_price,
            shipping_address=shipping_address,
            phone_number=phone_number,
            status='pending'
        )
        
        # สร้าง OrderItem
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.discounted_price
            )
            
            # อัปเดต sold_count
            item.product.sold_count += item.quantity
            item.product.save()
        
        # ล้างตะกร้า
        cart.items.all().delete()
        
        return redirect('chopee:order_detail', order_id=order.id)
    
    context = {'cart': cart}
    return render(request, 'chopee/checkout.html', context)

@login_required
def orders_list(request):
    """แสดงรายการคำสั่งซื้อของผู้ใช้"""
    orders = request.user.orders.all()
    context = {'orders': orders}
    return render(request, 'chopee/orders.html', context)

@login_required
def order_detail(request, order_id):
    """แสดงรายละเอียดคำสั่งซื้อ"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'chopee/order_detail.html', context)

@login_required
def add_review(request, product_id):
    """เพิ่มรีวิวสินค้า"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')
        
        review, created = Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                'rating': rating,
                'comment': comment,
            }
        )
        
        return redirect('chopee:product_detail', slug=product.slug)
    
    try:
        review = Review.objects.get(product=product, user=request.user)
    except Review.DoesNotExist:
        review = None
    
    context = {
        'product': product,
        'review': review,
    }
    return render(request, 'chopee/add_review.html', context)

@login_required
def user_profile(request):
    """แสดงและแก้ไขโปรไฟล์ผู้ใช้"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.phone_number = request.POST.get('phone_number', '')
        profile.address = request.POST.get('address', '')
        profile.city = request.POST.get('city', '')
        profile.postal_code = request.POST.get('postal_code', '')
        profile.save()
        return redirect('chopee:user_profile')
    
    context = {'profile': profile}
    return render(request, 'chopee/profile.html', context)

def shops_list(request):
    """แสดงรายการร้านค้า"""
    shops = Shop.objects.all()
    context = {'shops': shops}
    return render(request, 'chopee/shops.html', context)
