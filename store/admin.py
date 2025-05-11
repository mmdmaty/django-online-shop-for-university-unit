from django.contrib import admin
from .models import (
    Customer, Address, Category, Discount,
    Product, Attribute, AttributeValue,
    ProductVariant, ProductImages, Order,
    OrderItem, Comment, WishList
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'national_code', 'phone_number')
    search_fields = ('user__username', 'national_code', 'phone_number')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'city', 'postal_code', 'is_default')
    list_filter = ('city', 'is_default')
    search_fields = ('address', 'postal_code', 'city')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('name',)


class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date_time_created', 'date_time_modified')
    search_fields = ('name', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImagesInline]
    readonly_fields = ('date_time_created', 'date_time_modified')


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value', 'unit')
    list_filter = ('attribute',)
    search_fields = ('value',)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'inventory')
    filter_horizontal = ('attributes', 'discount',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'date_time_created')
    list_filter = ('status', 'date_time_created')
    search_fields = ('customer__user__username', 'id')
    readonly_fields = ('date_time_created', 'date_time_modified')
    inlines = [OrderItemInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'customer', 'rating', 'status', 'datetime_created')
    list_filter = ('status', 'rating')
    search_fields = ('body', 'customer__user__username', 'product__name')
    readonly_fields = ('datetime_created',)


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product')
    search_fields = ('customer__user__username', 'product__name')