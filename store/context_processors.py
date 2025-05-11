from .models import Category
from .cart import Cart

def category_tree(request):
    return {
        'categories': Category.objects.root_nodes()
    }


def cart(request):
    cart = Cart(request)
    return {
        'cart': cart
    }
