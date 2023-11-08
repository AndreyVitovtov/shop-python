from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from app.models import Product, Cart, Order, OrderItem

from app.views import totalPrice


# Create your views here.


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('productId')
        user = request.user
        product = Product.objects.get(id=product_id)
        cart_item, item_created = Cart.objects.get_or_create(customer=user, product=product)
        if not item_created:
            cart_item.count += 1
            cart_item.save()

        return JsonResponse({
            'sc': True,
            'count': Cart.objects.filter(customer=user).count() or 0
        })


@login_required
def countProductsInCart(request):
    if request.method == 'POST':
        user = request.user
        return JsonResponse({
            'sc': True,
            'count': Cart.objects.filter(customer=user).count() or 0
        })


@login_required
def removeFromCart(request):
    if request.method == 'POST':
        user = request.user
        product = Product.objects.get(id=request.POST.get('id'))
        cartItem = Cart.objects.filter(customer=user, product=product)
        cartItem.delete()
        return JsonResponse({
            'sc': True,
            'count': Cart.objects.filter(customer=user).count() or 0,
            'total_price': totalPrice(user)
        })


@login_required
def updateCountFromCart(request):
    if request.method == 'POST':
        user = request.user
        count = int(request.POST.get('count'))
        product = Product.objects.get(id=request.POST.get('id'))
        cartItem = Cart.objects.get(customer=user, product=product)
        if count < 1:
            cartItem.delete()
        else:
            cartItem.count = count
            cartItem.save()
        return JsonResponse({
            'sc': True,
            'count': Cart.objects.filter(customer=user).count() or 0,
            'total_price': totalPrice(user)
        })


@login_required
def checkout(request):
    order = Order(customer=request.user)
    order.save()
    cart_items = Cart.objects.filter(customer=request.user)
    for cart_item in cart_items:
        order_item = OrderItem(order=order, product=cart_item.product, count=cart_item.count)
        order_item.save()
    cart_items.delete()
    return JsonResponse({
        'sc': True
    })
