from django import template
from django.utils.html import format_html
from django.urls import reverse
from urllib.parse import quote
register = template.Library()


@register.filter(name="make_price")
def make_price(number:int)-> str:
    return f'{number:,}'




@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.simple_tag
def category_breadcrumb_links(category):
    breadcrumb = []
    while category:
        # encode نام دسته برای استفاده در URL (برای کاراکترهای فارسی و فاصله)
        category_name_encoded = quote(category.name)
        url = f'/home/?category={category_name_encoded}'
        link = f'<a href="{url}">{category.name}</a>'
        breadcrumb.insert(0, link)
        category = category.parent
    return format_html(' - '.join(breadcrumb))

if '__main__' == __name__:
    print(make_price(10000000000))