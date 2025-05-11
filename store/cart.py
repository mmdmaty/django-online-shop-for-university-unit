from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from .models import Product,ProductVariant


class Cart():
    def __init__(self, request: HttpRequest):
        self.request = request
        self.session = self.request.session
        cart = self.session.get('cart')
        if cart is None:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add_to_cart(self, product_variant, quantity,inplce=False, **kwargs):
        product_variant_id = str(product_variant.id)
        if product_variant_id in self.cart.keys():
            if inplce:
                self.cart[product_variant_id]['quantity'] = quantity
            else:
                self.cart[product_variant_id]['quantity'] += quantity
        else:
            self.cart[product_variant_id] = {"quantity": quantity,
                                     'attributes': kwargs,}
            

        self.update_cart()


    def update_cart(self):
        self.session.modified = True

    # def delete_item_form_cart(self, product):
    #     product_id = str(product.id)
    #     del self.cart[product_id]
    #     self.update_cart()

    def clean_cart(self):
        del self.session['cart']

    def __iter__(self):

        products = self.cart.keys()
        products = ProductVariant.objects.filter(id__in=products).select_related('product')
        cart = self.cart.copy()
        for product in products:
            self.cart[str(product.id)]['product_obj'] = product
        for item in self.cart.values():
            item['object_total_price'] = item['product_obj'].get_discounted_price() * \
                item['quantity']

            yield item

    def __len__(self):
        return len(self.cart.keys())

    def cart_total_price_without_discount(self):
        total = 0
        for product_id, item in self.cart.items():
            product = get_object_or_404(ProductVariant, id=product_id)
            total += product.price * item['quantity']
        return int(total)

    def cart_total_price_with_discount(self):
        total = 0
        for product_id, item in self.cart.items():
            product = get_object_or_404(ProductVariant, id=product_id)
            total += product.get_discounted_price() * item['quantity']
        return int(total)

    def cart_total_discount(self):
        return self.cart_total_price_without_discount() - self.cart_total_price_with_discount()
    
    @property
    def is_empty(self):
        return len(self) == 0

