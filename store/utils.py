# app/utils.py
from slugify import slugify as awesome_slugify

def slugify_persian(text):
    """
    تابع تبدیل متن فارسی به اسلاگ معتبر
    """
    # تنظیمات اختصاصی برای فارسی
    replacements = [
        ('ـ', ''),  # حذف کشیده
        ('‌', '-'),  # فاصله مجازی به خط تیره
        (' ', '-'),  # فاصله معمولی به خط تیره
    ]
    
    # انجام جایگزینی‌های سفارشی
    for old, new in replacements:
        text = text.replace(old, new)
    
    # تبدیل به اسلاگ با پشتیبانی از یونیکد
    slug = awesome_slugify(
        text,
        lowercase=False,
        separator='-',
        replacements=[('ـ', ''), ('‌', '-')],
        allow_unicode=True
    )
    
    return slug