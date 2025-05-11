from django.shortcuts import render, get_object_or_404, redirect
from datetime import date
from django.views import generic
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from .cart import Cart


class ProductListView(generic.ListView):
    model = models.Product
    template_name = 'store/home.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # for product in context['products']:
        #     product.discounted_price = product.get_discounted_price()

        return context

    def get_queryset(self):
        if self.request.GET.get('category') is not None:
            return models.Product.objects.filter(category__name=self.request.GET.get('category'))
        return super().get_queryset()

# class ProductDetailViews(generic.DetailView):
#     model = models.Product
#     template_name = 'store/product-details.html'
#     context_object_name = 'product'

def product_detail(request, slug):
    product = get_object_or_404(models.Product, slug=slug)
    variants = product.productvariant_set.all()  # همه واریانت‌های محصول
    context = {
        'product': product,
        'variants': variants,
        'default_variant': product.default_variant,
    }
    return render(request, 'store/product-details.html', context)


def add_to_cart_views(request: HttpRequest):
    cart = Cart(request=request)

    if request.method == 'POST':
        print(request.POST)
        form = forms.AddCartForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # print('ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt')
            quantity = form.cleaned_data.get('quantity')
            product_variant_id = form.cleaned_data.get('variant_id')
            product_variant = models.ProductVariant.objects.get(id = product_variant_id)
        else:
            print(form.errors)
        print(form.cleaned_data.get('inplace'))
    cart.add_to_cart(product_variant=product_variant, quantity=quantity,
                     inplce=form.cleaned_data.get('inplace'))
    return redirect('cart')


def showcart(request):
    cart = Cart(request=request)
    for item in cart:
        item['inplace_form'] = forms.AddCartForm(initial={
            'quantity': 1,
            'inplace': 'True'
        })
    form = forms.AddCartForm(initial={'inplce': True})
    return render(request=request, template_name='store/cart.html', context={'cart': cart, 'form': form})


def remove_item_cart(request, slug):
    cart = Cart(request=request)
    product = get_object_or_404(models.Product, slug=slug)
    cart.delete_item_form_cart(product=product)
    return redirect('cart')


def clean_cart(request):
    cart = Cart(request=request)
    cart.clean_cart()
    return redirect('home')


class WishListView(generic.ListView):
    template_name = 'store/wishlist.html'
    model = models.WishList
    context_object_name = 'wish'

    def get_queryset(self):
        return models.WishList.objects.filter(customer__user = self.request.user).select_related('product').prefetch_related('product__discounts','product__image')


def remove_from_wishlist(request,slug):
    product = models.Product.objects.get(slug = slug)
    instance = models.WishList.objects.get(customer__user = request.user,product=product)
    instance.delete()
    return redirect('wish')



from django.http import HttpResponse
@login_required
def Order_accept(request):
    cart = Cart(request=request)
    user = request.user
    customer = get_object_or_404(models.Customer,user = user)
    if request.method == 'GET':

        form = forms.OrderForm(customer = customer)
        default_address = models.Address.objects.filter(customer=customer, is_default=True).first()
        return render(request=request,template_name='store/checkout.html',context={'form':form,'default_address':default_address})
    else:
        form = forms.OrderForm(data=request.POST,customer = customer)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            order.postal_code = order.shipping_address.postal_code
            order.total_price = cart.cart_total_price_with_discount()
            order.save()
            for item in cart:
                order_item = models.OrderItem()
                order_item.product = item['product_obj']
                order_item.order = order
                order_item.price = item['product_obj'].price
                order_item.quantity = item['quantity']
                order_item.save()
            cart.clean_cart()
        return HttpResponse('created')



def add_address(request):
    user = request.user
    customer = get_object_or_404(models.Customer,user = user)
    if request.method == 'GET':
        form = forms.AddressFrom()
    else:
        form = forms.AddressFrom(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = customer
            address.is_default = True if customer.addresses else False 
            address.save()
            return redirect('check_out')
    return render(request=request,template_name='store/add_address.html',context={'form':form})