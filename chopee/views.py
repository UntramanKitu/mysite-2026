from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.files.base import ContentFile
from django.utils.text import slugify
from decimal import Decimal

from .models import Product, Category, UserProfile, Cart, CartItem, Order, Shop


def ensure_user_cart(user):
    if not user.is_authenticated:
        return None
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def seed_mock_products():
    """สร้างข้อมูลตัวอย่าง 5 สินค้าเพื่อให้หน้าแสดงผลเหมือน Shopeeทันที"""
    if Product.objects.exists():
        return

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

    seller_user, _ = User.objects.get_or_create(username='demo-seller')
    shop, _ = Shop.objects.get_or_create(
        owner=seller_user,
        defaults={
            'shop_name': 'Chopee Demo Shop',
            'description': 'ร้านค้าตัวอย่างสำหรับแสดงผล',
        },
    )

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
    if request.user.is_authenticated:
        ensure_user_cart(request.user)

    products = Product.objects.all()
    categories = Category.objects.all()

    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)

    sort = request.GET.get('sort', '-id')
    products = products.order_by(sort)

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'chopee/products.html', context)


def product_detail(request, slug):
    """แสดงรายละเอียดสินค้า"""
    if request.user.is_authenticated:
        ensure_user_cart(request.user)

    product = get_object_or_404(Product, slug=slug)
    context = {'product': product}
    return render(request, 'chopee/product_detail.html', context)


@login_required
def user_profile(request):
    """แสดงหน้าโปรไฟล์ผู้ใช้"""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    ensure_user_cart(request.user)
    return render(request, 'chopee/profile.html', {'profile': profile})


@login_required
def cart(request):
    """แสดงหน้าเพจตะกร้า"""
    cart_obj = ensure_user_cart(request.user)
    return render(request, 'chopee/cart.html', {'cart': cart_obj})


@login_required
def add_to_cart(request, pk):
    """เพิ่มสินค้าเข้าในตะกร้า"""
    product = get_object_or_404(Product, pk=pk)
    cart_obj = ensure_user_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart_obj, product=product, defaults={'quantity': 1})
    if not created:
        item.quantity += 1
        item.save()
    return redirect('chopee:cart')


@login_required
def update_cart_item(request, item_id):
    """อัปเดตจำนวนสินค้าในตะกร้า"""
    cart_obj = ensure_user_cart(request.user)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart_obj)
    quantity = request.POST.get('quantity', 1)
    item.quantity = max(1, int(quantity))
    item.save()
    return redirect('chopee:cart')


@login_required
def remove_from_cart(request, item_id):
    """ลบสินค้าออกจากตะกร้า"""
    cart_obj = ensure_user_cart(request.user)
    CartItem.objects.filter(pk=item_id, cart=cart_obj).delete()
    return redirect('chopee:cart')


@login_required
def checkout(request):
    """หน้าชำระเงินตัวอย่าง"""
    cart_obj = ensure_user_cart(request.user)
    return render(request, 'chopee/checkout.html', {'cart': cart_obj})


@login_required
def orders_list(request):
    """แสดงรายการคำสั่งซื้อ"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'chopee/orders.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    """แสดงรายละเอียดคำสั่งซื้อ"""
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'chopee/order_detail.html', {'order': order})


def shop_detail(request, pk):
    """แสดงรายละเอียดร้านค้า"""
    if request.user.is_authenticated:
        ensure_user_cart(request.user)

    shop = get_object_or_404(Shop, pk=pk)
    products = Product.objects.filter(shop=shop)
    return render(request, 'chopee/shop_detail.html', {'shop': shop, 'products': products})


def shops_list(request):
    """แสดงรายการร้านค้า"""
    if request.user.is_authenticated:
        ensure_user_cart(request.user)

    shops = Shop.objects.all()
    return render(request, 'chopee/shops.html', {'shops': shops})
