from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.files.base import ContentFile
from django.utils.text import slugify
from decimal import Decimal

from .models import Product, Category

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
            category=item['category'],
            name=item['name'],
            description=item['description'],
            price=item['price'],
            original_price=item['price'] * Decimal('1.2'),
            image=make_svg(item['name'], item['bg'], item['text']).name,
            rating=item['rating'],
            sold_count=item['sold_count'],
            stock=item['stock'],
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
    sort = request.GET.get('sort', '-id')
    if sort in {'-created_at', 'created_at'}:
        sort = '-id'
    if sort in {'price', '-price', '-sold_count'}:
        products = products.order_by(sort)
    else:
        products = products.order_by(sort)
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'chopee/products.html', context)

def product_detail(request, pk):
    """แสดงรายละเอียดสินค้า"""
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'chopee/product_detail.html', context)


def shops_list(request):
    """แสดงรายการร้านค้า"""
    return render(request, 'chopee/shops.html', {'shops': []})
