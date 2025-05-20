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
        category_name = self.request.GET.get('category')
        if category_name:
            try:
                # دسته والد
                category = models.Category.objects.get(name=category_name)

                # همه دسته‌های زیرمجموعه (خودش + فرزندان و نوه‌ها)
                all_categories = category.get_descendants(include_self=True)

                return models.Product.objects.filter(category__in=all_categories)
            except models.Category.DoesNotExist:
                return models.Product.objects.none()  # اگر دسته‌ای با این اسم نبود، چیزی نشون نده
        return super().get_queryset()

class ProductDetailViews(generic.DetailView):
    model = models.Product
    template_name = 'store/product-details.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['variants'] = context['product'].productvariant_set.all()
        context['default_variant'] = context['product'].default_variant
        context['comments'] = context['product'].comments.filter(status = models.Comment.COMMENT_STATUS_APPROVED)
        return context
    
    def post(self, request, *args, **kwargs):
        product = self.get_object()
        if self.request.user.is_authenticated:
            user = self.request.user
            customer = get_object_or_404(models.Customer,user = user)
            form = forms.Comments(self.request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.product = product
                comment.customer = customer
                comment.save()
        return redirect('product_details',slug = product.slug)




def add_to_cart_views(request: HttpRequest):
    cart = Cart(request=request)

    if request.method == 'POST':
        print(request.POST)
        form = forms.AddCartForm(request.POST)
        if form.is_valid():
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
        return models.WishList.objects.filter(customer__user = self.request.user).select_related('product')


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
    customer = get_object_or_404(models.Customer, user=user)
    
    if request.method == 'GET':
        form = forms.OrderForm(customer=customer)
        default_address = models.Address.objects.filter(customer=customer, is_default=True).first()
        return render(request=request, template_name='store/checkout.html', context={'form': form, 'default_address': default_address})
    else:
        form = forms.OrderForm(data=request.POST, customer=customer)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            order.postal_code = order.shipping_address.postal_code
            order.total_price = cart.cart_total_price_with_discount()
            order.save()
            
            
            # Creating Order Items
            for item in cart:
                order_item = models.OrderItem()
                order_item.product_variant = item['product_obj']
                order_item.order = order
                order_item.price = item['product_obj'].price
                order_item.quantity = item['quantity']
                order_item.save()
                
            cart.clean_cart()
            return redirect('payment',order_id=order.id)
        else:
            return render(request, 'store/checkout.html', {'form': form, 'default_address': default_address})




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
            address.is_default = False if customer.addresses.exists() else True 
            address.save()
            return redirect('check_out')
    return render(request=request,template_name='store/add_address.html',context={'form':form})

def payment(request,order_id):
    if request.method == "POST":
        form = forms.PaymentForm(request.POST)
        if form.is_valid():
            
            customer = models.Customer.objects.get(user=request.user)
            order = models.Order.objects.get(id = order_id,customer=customer)
            if order:
                order.status = models.Order.ORDER_STATUS_COMPLETED
                order.save()
            return redirect('order_show',pk= order_id)
    else:
        form = forms.PaymentForm()
        return render(request, 'store/payment.html', {'form': form})


class OrderDitails(generic.DeleteView):
    model = models.Order
    template_name = 'store/order_show.html'
    context_object_name = 'order'
    def get_queryset(self):
        return models.Order.objects.filter(id = self.kwargs.get('pk'),customer = models.Customer.objects.get(user = self.request.user))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self.get_object().items.all()
        return context
    
def contact_us(request):
    return render(request=request,template_name='store/contact-us.html')

def add_to_wish(request,slug):
    wish = models.WishList()
    wish.customer = get_object_or_404(models.Customer,user = request.user)
    wish.product = get_object_or_404(models.Product,slug = slug)
    wish.save()
    return redirect('product_details',slug = slug)


# views.py
from django.http import JsonResponse
from .models import Product

def live_search(request):
    q = request.GET.get('q', '')
    results = []
    if q:
        for product in Product.objects.filter(name__icontains=q)[:10]:
            results.append({'slug': product.slug, 'name': product.name})
    return JsonResponse({'results': results})

