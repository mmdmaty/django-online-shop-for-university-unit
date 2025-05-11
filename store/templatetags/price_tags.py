from django import template
register = template.Library()


@register.filter(name="make_price")
def make_price(number:int)-> str:
    return f'{number:,}'




@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

if '__main__' == __name__:
    print(make_price(10000000000))