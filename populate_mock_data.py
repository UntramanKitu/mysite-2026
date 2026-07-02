import os
import shutil
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite2026.settings')
django.setup()

from django.contrib.auth.models import User
from chopee.models import Shop, Category, Product
from django.utils.text import slugify

# Paths
SRC_DIR = r"C:\Users\ASUS_TUF\.gemini\antigravity-ide\brain\b009dfe3-da49-4089-8538-48a07eb0ea73"
MEDIA_DIR = r"d:\Web\mysite-2026\media\product_images"

# 1. Create Media Directory
os.makedirs(MEDIA_DIR, exist_ok=True)

# 2. Copy files
images = {
    'smartphone_promax_1782987184850.png': 'smartphone.png',
    'wireless_headphones_1782987219340.png': 'headphones.png',
    'ergonomic_chair_1782988439223.png': 'chair.png',
}

for src_name, dest_name in images.items():
    src_path = os.path.join(SRC_DIR, src_name)
    dest_path = os.path.join(MEDIA_DIR, dest_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, dest_path)
        print(f"Copied {src_name} to {dest_path}")
    else:
        print(f"Source file not found: {src_path}")

# 3. Clear existing data to avoid conflicts
Product.objects.all().delete()
Category.objects.all().delete()
Shop.objects.all().delete()

# 4. Create Admin / Shop Owner User
username = 'admin'
email = 'admin@example.com'
password = 'admin1234'

user, created = User.objects.get_or_create(username=username, email=email)
if created:
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"User {username} created successfully.")
else:
    print(f"User {username} already exists.")

# 4. Create Shop
shop, created = Shop.objects.get_or_create(
    owner=user,
    defaults={
        'shop_name': 'Chopee Official Store',
        'description': 'ร้านค้าอย่างเป็นทางการ รวบรวมสินค้าคุณภาพดีที่สุดสำหรับคุณ',
        'follow_count': 1250,
        'rating': 4.9
    }
)
if created:
    print("Shop 'Chopee Official Store' created.")
else:
    print("Shop 'Chopee Official Store' already exists.")

# 5. Create Categories
cat_electronics, _ = Category.objects.get_or_create(
    name='เครื่องใช้ไฟฟ้าและอิเล็กทรอนิกส์',
    defaults={'slug': 'electronics', 'description': 'โทรศัพท์ คอมพิวเตอร์ หูฟัง และอุปกรณ์อิเล็กทรอนิกส์อื่นๆ'}
)

cat_home, _ = Category.objects.get_or_create(
    name='ของแต่งบ้านและเฟอร์นิเจอร์',
    defaults={'slug': 'home-living', 'description': 'เฟอร์นิเจอร์ ของแต่งบ้าน และเครื่องใช้ในครัวเรือน'}
)
print("Categories created/verified.")

# 6. Create Products
products_data = [
    {
        'shop': shop,
        'category': cat_electronics,
        'name': 'iPhone 15 Pro Max (Mockup)',
        'slug': 'iphone-15-pro-max-mockup',
        'description': 'สมาร์ทโฟนระดับเรือธง มาพร้อมกับกล้อง 3 ตัวสุดล้ำ หน้าจอที่สว่างเป็นพิเศษ ชิปประมวลผลความเร็วสูง และดีไซน์วัสดุไทเทเนียมสุดหรูหรา',
        'price': 45900.00,
        'discount_percentage': 5,
        'stock': 10,
        'image': 'product_images/smartphone.png',
        'rating': 4.8,
        'sold_count': 23,
    },
    {
        'shop': shop,
        'category': cat_electronics,
        'name': 'Sony WH-1000XM5 (Mockup)',
        'slug': 'sony-wh-1000xm5-mockup',
        'description': 'หูฟังไร้สายขจัดเสียงรบกวนชั้นนำรุ่นล่าสุด ให้คุณดื่มด่ำกับเสียงเพลงอย่างไร้เสียงรบกวน แบตเตอรี่ยาวนานสูงสุด 30 ชั่วโมง สวมใส่สบายตลอดทั้งวัน',
        'price': 11900.00,
        'discount_percentage': 10,
        'stock': 15,
        'image': 'product_images/headphones.png',
        'rating': 4.9,
        'sold_count': 45,
    },
    {
        'shop': shop,
        'category': cat_home,
        'name': 'Ergonomic Office Chair (Mockup)',
        'slug': 'ergonomic-office-chair-mockup',
        'description': 'เก้าอี้ทำงานเพื่อสุขภาพ ปรับเปลี่ยนระดับตามสรีระได้หลากหลาย จุดรองรับส่วนเอวและคอออกแบบอย่างเหมาะสม พนักพิงผ้าตาข่ายระบายอากาศได้ดีเยี่ยม ช่วยลดอาการออฟฟิศซินโดรม',
        'price': 6500.00,
        'discount_percentage': 12,
        'stock': 8,
        'image': 'product_images/chair.png',
        'rating': 4.7,
        'sold_count': 12,
    }
]

for p_data in products_data:
    p, created = Product.objects.update_or_create(
        slug=p_data['slug'],
        defaults=p_data
    )
    if created:
        print(f"Product '{p.name}' created.")
    else:
        print(f"Product '{p.name}' updated.")

print("All mock data seeded successfully!")
