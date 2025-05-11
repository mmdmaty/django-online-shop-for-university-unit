from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
from .utils import slugify_persian
from django.contrib.auth import get_user_model
from django.utils.timezone import now

class Customer(models.Model):
    user = models.OneToOneField(
        to=get_user_model(), on_delete=models.CASCADE, related_name='customers')
    national_code = models.CharField(
        max_length=10,
        verbose_name=_('national code'),
        unique=True,
        blank=True,
        null=True
    )
    phone_number = PhoneNumberField(
        verbose_name=_('phone number'),
        unique=True,
        region='IR',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')

    def __str__(self):
        return f"{self.user} "


class Address(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name=_('customer'),
        related_name='addresses'
    )
    address = models.TextField(verbose_name=_('address'))
    postal_code = models.CharField(
        max_length=10, verbose_name=_('postal code'))
    city = models.CharField(max_length=50, verbose_name=_('city'))
    is_default = models.BooleanField(
        default=False, verbose_name=_('default address'))

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')

    def __str__(self):
        return f"{self.address}, {self.city}"


class Category(MPTTModel):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    slug = models.SlugField(max_length=220, unique=True,
                            allow_unicode=True, verbose_name=_('slug'))
    description = models.TextField(
        blank=True, null=True, verbose_name=_('description'))
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('parent category')
    )
    top_product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_('top product'))

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_persian(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('name'))
    discount = models.FloatField(verbose_name=_('discount percentage'))
    description = models.TextField(
        blank=True, null=True, verbose_name=_('description'))
    start_date = models.DateTimeField(verbose_name=_('start date'))
    end_date = models.DateTimeField(verbose_name=_('end date'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))

    class Meta:
        verbose_name = _('discount')
        verbose_name_plural = _('discounts')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=220, unique=True,
                            allow_unicode=True, verbose_name=_('slug'))
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_modified = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(to=Category,on_delete=models.PROTECT)
    discription = models.TextField()
    default_variant = models.OneToOneField(to='ProductVariant',on_delete=models.PROTECT,related_name='+',null=True,blank=True)

class Attribute(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name}"

class AttributeValue(models.Model):
    attribute = models.ForeignKey(to=Attribute,on_delete=models.PROTECT)
    value = models.CharField(max_length=150)
    unit = models.CharField(max_length=150,blank=True)

    def __str__(self):
        return f"{self.attribute.name}-{self.value}"

class ProductVariant(models.Model):
    product = models.ForeignKey(to=Product,on_delete=models.PROTECT)
    attributes = models.ManyToManyField(to=AttributeValue)
    price = models.PositiveIntegerField()
    inventory = models.PositiveIntegerField()
    discount = models.ManyToManyField(to=Discount,blank=True)


    def __str__(self):
        return f'{self.product.name} - {" - ".join(str(at.value) for at in self.attributes.all())}'

    def get_discounted_price(self):
        active_discounts = self.discount.all()  # اضافه کردن فیلتر برای تخفیف‌های فعال
        
        if not active_discounts.exists():
            return self.price
        
        # یا بیشترین تخفیف را اعمال کنید:
        max_discount = max([d.discount for d in active_discounts])
        # یا فقط اولین تخفیف را اعمال کنید:
        # first_discount = active_discounts.first().discount
        
        total_discount_percent = min(max_discount, 100)  # اطمینان از عدم превыص ۱۰۰٪
        discounted_price = self.price * (1 - total_discount_percent / 100)
        
        return round(discounted_price)  # بهتر است از round به جای int استفاده شود



class ProductImages(models.Model):
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        verbose_name=_('product image'))


class Order(models.Model):
    ORDER_STATUS_PENDING = 'pending'
    ORDER_STATUS_PROCESSING = 'processing'
    ORDER_STATUS_COMPLETED = 'completed'
    ORDER_STATUS_CANCELLED = 'cancelled'

    ORDER_STATUS_CHOICES = [
        (ORDER_STATUS_PENDING, _('Pending')),
        (ORDER_STATUS_PROCESSING, _('Processing')),
        (ORDER_STATUS_COMPLETED, _('Completed')),
        (ORDER_STATUS_CANCELLED, _('Cancelled')),
    ]

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('customer'))

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    postal_code = models.CharField(
        max_length=10, verbose_name=_('postal code'))

    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES,
                              default=ORDER_STATUS_PENDING, verbose_name=_('status'))

    total_price = models.PositiveIntegerField(verbose_name=_('total price'))

    shipping_address = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name='orders', verbose_name=_('shipping address'))

    date_time_created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))

    date_time_modified = models.DateTimeField(
        auto_now=True, verbose_name=_('updated at'))

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
        ordering = ['-date_time_created']

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"


class OrderItem(models.Model):
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        related_name='order_items',
        verbose_name=_('product'))
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('order'))
    price = models.PositiveIntegerField(verbose_name=_('price'))
    quantity = models.PositiveIntegerField(
        verbose_name=_('quantity'),
        default=1
    )

    class Meta:
        unique_together = [['order', 'product_variant']]
        verbose_name = _('order item')
        verbose_name_plural = _('order items')

    def __str__(self):
        return f"{self.quantity}x {self.product_variant.product.name}"


class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'na'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, _('Waiting')),
        (COMMENT_STATUS_APPROVED, _('Approved')),
        (COMMENT_STATUS_NOT_APPROVED, _('Not Approved')),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('product'))
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('customer'))
    body = models.TextField(verbose_name=_('body'))
    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name=_('rating'))
    datetime_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'))
    status = models.CharField(
        max_length=2,
        choices=COMMENT_STATUS,
        default=COMMENT_STATUS_WAITING,
        verbose_name=_('status'))

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['-datetime_created']

    def __str__(self):
        return f"{self.body} by {self.customer}"


class WishList(models.Model):
    product = models.ForeignKey(
        to=Product, on_delete=models.CASCADE, related_name='wishes')
    customer = models.ForeignKey(
        to=Customer, on_delete=models.PROTECT, related_name='user_wishes')
