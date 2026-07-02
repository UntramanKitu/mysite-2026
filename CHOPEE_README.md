# Chopee - E-Commerce Platform

Chopee คือ แพลตฟอร์มอีคอมเมิร์สที่ออกแบบมาเพื่อให้ผู้ขายและผู้ซื้อสามารถทำการซื้อขายสินค้าออนไลน์ได้อย่างสะดวก คล้ายกับ Shopee

## ฟีเจอร์หลัก

### สำหรับผู้ซื้อ
- 🛍️ **ดูรายการสินค้า** - ค้นหาและกรองสินค้าตามหมวดหมู่
- 🛒 **ตะกร้าสินค้า** - เพิ่มลบและปรับปรุงสินค้าในตะกร้า
- 💳 **ชำระเงิน** - ระบบการชำระเงินที่ง่ายและปลอดภัย
- 📦 **ติดตามคำสั่งซื้อ** - ดูสถานะการจัดส่ง
- ⭐ **เขียนรีวิว** - ให้คะแนนและเขียนความเห็น
- 👤 **โปรไฟล์ผู้ใช้** - จัดการข้อมูลส่วนตัวและที่อยู่
- 🏪 **ติดตามร้านค้า** - ติดตามร้านค้าที่ชื่นชอบ

### สำหรับผู้ดูแลระบบ
- 📊 **Dashboard** - Django Admin สำหรับจัดการสินค้าและคำสั่ง
- 👥 **จัดการผู้ใช้** - สร้าง แก้ไข ลบผู้ใช้
- 🏪 **จัดการร้านค้า** - สร้างและแก้ไขร้านค้า
- 📦 **จัดการสินค้า** - เพิ่มสินค้า แก้ไขราคา สต็อก
- 🎯 **จัดการหมวดหมู่** - สร้างหมวดหมู่สินค้า

## โครงสร้าง

```
chopee/
├── models.py           # โมเดลฐานข้อมูล
├── views.py            # ฟังก์ชัน views
├── urls.py             # URL routing
├── admin.py            # Django admin configuration
├── apps.py             # App configuration
├── migrations/         # Database migrations
└── templatetags/       # Custom template tags
    ├── __init__.py
    └── custom_filters.py
```

## โมเดล (Models)

### Shop (ร้านค้า)
- `owner` - เจ้าของร้าน (User)
- `shop_name` - ชื่อร้านค้า
- `shop_avatar` - รูปโปรไฟล์ร้าน
- `shop_banner` - แบนเนอร์ร้าน
- `description` - คำอธิบายร้าน
- `rating` - คะแนนร้าน (0-5)
- `follow_count` - จำนวนผู้ติดตาม

### Product (สินค้า)
- `shop` - ร้านค้า (Foreign Key)
- `category` - หมวดหมู่ (Foreign Key)
- `name` - ชื่อสินค้า
- `description` - คำอธิบายสินค้า
- `price` - ราคาเต็ม
- `discount_percentage` - ส่วนลด (%)
- `stock` - จำนวนสต็อก
- `image` - รูปภาพหลัก
- `rating` - คะแนนสินค้า

### Category (หมวดหมู่)
- `name` - ชื่อหมวดหมู่
- `slug` - URL slug
- `icon` - ไอคอนหมวดหมู่
- `description` - คำอธิบาย

### Cart (ตะกร้าสินค้า)
- `user` - ผู้ใช้ (One to One)
- `items` - สินค้าในตะกร้า (Related)

### CartItem (สินค้าในตะกร้า)
- `cart` - ตะกร้า (Foreign Key)
- `product` - สินค้า (Foreign Key)
- `quantity` - จำนวน

### Order (คำสั่งซื้อ)
- `user` - ผู้ซื้อ (Foreign Key)
- `order_number` - เลขที่คำสั่ง
- `status` - สถานะ (pending, paid, shipping, delivered, cancelled)
- `total_price` - ราคารวม
- `shipping_address` - ที่อยู่จัดส่ง
- `phone_number` - เบอร์โทรศัพท์

### OrderItem (สินค้าในคำสั่ง)
- `order` - คำสั่งซื้อ (Foreign Key)
- `product` - สินค้า (Foreign Key)
- `quantity` - จำนวน
- `price` - ราคาที่ซื้อ

### Review (รีวิวสินค้า)
- `product` - สินค้า (Foreign Key)
- `user` - ผู้เขียน (Foreign Key)
- `rating` - คะแนน (1-5)
- `comment` - ความเห็น
- `image` - รูปภาพรีวิว

### UserProfile (โปรไฟล์ผู้ใช้)
- `user` - ผู้ใช้ (One to One)
- `phone_number` - เบอร์โทรศัพท์
- `address` - ที่อยู่
- `city` - เมือง
- `postal_code` - รหัสไปรษณีย์
- `followed_shops` - ร้านค้าที่ติดตาม (Many to Many)

## URL Routes

```
/chopee/                              - หน้าแรก (รายการสินค้า)
/chopee/product/<slug>/               - หน้ารายละเอียดสินค้า
/chopee/shop/<shop_id>/               - หน้าร้านค้า
/chopee/shops/                        - รายการร้านค้าทั้งหมด
/chopee/cart/                         - ตะกร้าสินค้า
/chopee/cart/add/<product_id>/        - เพิ่มสินค้าลงตะกร้า
/chopee/cart/update/<item_id>/        - อัปเดตจำนวนสินค้า
/chopee/cart/remove/<item_id>/        - ลบสินค้าจากตะกร้า
/chopee/checkout/                     - หน้าชำระเงิน
/chopee/orders/                       - รายการคำสั่งซื้อ
/chopee/order/<order_id>/             - รายละเอียดคำสั่งซื้อ
/chopee/product/<product_id>/review/  - เขียนรีวิว
/chopee/profile/                      - โปรไฟล์ผู้ใช้
```

## การติดตั้งและใช้งาน

### 1. ติดตั้ง

```bash
# ติดตั้ง dependencies
pip install django pillow

# สร้าง migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 2. สร้าง Admin User

```bash
python manage.py createsuperuser
```

### 3. เพิ่มข้อมูลเริ่มต้น

ไปที่ Django Admin (`/admin/`) และสร้าง:
- **Shop** - สร้างร้านค้า
- **Category** - สร้างหมวดหมู่
- **Product** - เพิ่มสินค้า

### 4. รันเซิร์ฟเวอร์

```bash
python manage.py runserver
```

จากนั้นเข้าไปที่ `http://localhost:8000/chopee/`

## Setting ที่ปรับเปลี่ยน

ในไฟล์ `settings.py` ได้ทำการปรับเปลี่ยน:

```python
INSTALLED_APPS = [
    ...
    'chopee',
]

LANGUAGE_CODE = 'th-TH'
TIME_ZONE = 'Asia/Bangkok'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## Template Tags

### Custom Filter: `mul`

ใช้สำหรับการคูณค่าในเทมเพลต:

```html
{% load custom_filters %}
{{ price|mul:quantity }}
```

## ไฟล์และโฟลเดอร์

```
templates/chopee/
├── base.html              - เทมเพลตพื้นฐาน
├── products.html          - รายการสินค้า
├── product_detail.html    - รายละเอียดสินค้า
├── cart.html              - ตะกร้าสินค้า
├── checkout.html          - ชำระเงิน
├── orders.html            - รายการคำสั่ง
├── order_detail.html      - รายละเอียดคำสั่ง
├── shop_detail.html       - หน้าร้านค้า
├── shops.html             - รายการร้านค้า
├── add_review.html        - เขียนรีวิว
└── profile.html           - โปรไฟล์ผู้ใช้

media/
├── product_images/        - รูปสินค้า
├── shop_avatars/          - รูปโปรไฟล์ร้าน
├── shop_banners/          - แบนเนอร์ร้าน
├── review_images/         - รูปรีวิว
└── user_avatars/          - รูปโปรไฟล์ผู้ใช้
```

## ฟีเจอร์ที่อาจเพิ่มเติมในอนาคต

- [ ] ระบบ Payment Gateway (ตัวจริง)
- [ ] ระบบ Chat Seller-Buyer
- [ ] ระบบ Wishlist
- [ ] ระบบ Voucher/Coupon
- [ ] ระบบ Shipping Integration
- [ ] Admin Dashboard (สถิติ, รายงาน)
- [ ] Mobile App
- [ ] ระบบ Notification
- [ ] Advanced Search & Filter

## การแก้ไขปัญหาทั่วไป

### ปัญหา: ไม่สามารถอัปโหลดรูปภาพ
**วิธีแก้**: ตรวจสอบว่า `MEDIA_ROOT` มีสิทธิในการเขียน และ Pillow ติดตั้งแล้ว

### ปัญหา: รูปภาพไม่แสดง
**วิธีแก้**: ตรวจสอบ `MEDIA_URL` ใน settings.py และ URL configuration

### ปัญหา: เกิด Error ที่ Template
**วิธีแก้**: ตรวจสอบว่า `{% load custom_filters %}` อยู่ที่ด้านบนของเทมเพลต

## ลิขสิทธิ์

ปรับปรุงเพื่อการเรียนรู้ Django Framework

## ติดต่อ

หากมีคำถามหรือเสนอแนะ โปรดติดต่อ Chopee Team
