from django.urls import path
from . import views



urlpatterns = [
    path(route='home/',view=views.ProductListView.as_view(),name='home'),
    path(route='product/<slug:slug>/',view=views.ProductDetailViews.as_view(),name='product_details'),
    path(route='cart/add_to_cart/',view=views.add_to_cart_views,name=('cart__add_to_cart')),
    path(route='cart/',view=views.showcart,name='cart'),
    path(route='cart/remove_item_from_cart/<slug:slug>/',view=views.remove_item_cart,name=('cart__remove_from_cart')),
    path(route='clean_cart/',view=views.clean_cart,name='clean_cart'),
    path(route='wish_list/',view=views.WishListView.as_view(),name='wish'),
    path(route='remove_itme_from_wish_list/<slug:slug>',view=views.remove_from_wishlist,name='remove_form_wish_list'),
    path(route='check_out/',view=views.Order_accept,name='check_out'),
    path(route='add_address/',view=views.add_address,name='add_address'),
    path(route='order_show/<int:pk>/',view=views.OrderDitails.as_view(),name='order_show'),
    path(route='payment/<int:order_id>/',view=views.payment,name='payment'),
]