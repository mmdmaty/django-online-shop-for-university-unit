from django.test import RequestFactory
from store.cart import Cart
from store import models
from django.contrib.sessions.middleware import SessionMiddleware

# ایجاد ویژگی‌ها
color = models.Attribute.objects.create(name="رنگ")
memory = models.Attribute.objects.create(name="حافظه")
weight = models.Attribute.objects.create(name="وزن")

# ایجاد مقادیر ویژگی‌ها
black = models.AttributeValue.objects.create(attribute=color, value="مشکی")
white = models.AttributeValue.objects.create(attribute=color, value="سفید")
gb128 = models.AttributeValue.objects.create(attribute=memory, value="128GB")
gb256 = models.AttributeValue.objects.create(attribute=memory, value="256GB")
weight_200g = models.AttributeValue.objects.create(attribute=weight, value="200 گرم")

# ایجاد محصول پایه
phone = models.Product.objects.create(
    name="گوشی موبایل سامسونگ گلکسی S22",
    description="گوشی هوشمند سری S سامسونگ",
    is_active=True
)

# افزودن ویژگی مشترک (وزن)
models.ProductCommonAttribute.objects.create(
    product=phone,
    attribute=weight,
    value=weight_200g
)

# ایجاد انواع محصول
variant1 = models.ProductVariant.objects.create(
    product=phone,
    sku="S22-BLACK-128",
    price=25000000,
    stock=10,
    is_active=True
)
variant1.attributes.add(black, gb128)

variant2 = models.ProductVariant.objects.create(
    product=phone,
    sku="S22-WHITE-256",
    price=28000000,
    stock=5,
    is_active=True
)
variant2.attributes.add(white, gb256)
