import os
import json
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Cart, Product, Category, Subcategory


def totalPrice(user):
    total = 0
    for c in Cart.objects.filter(customer=user):
        total += c.product.price * c.count
    return round(total, 2)


# Create your views here.

def images_exists(product):
    print(os.path.join(settings.STATICFILES_DIRS[0], 'images',
                       product['image']))
    product['image'] = product['image'] if os.path.exists(os.path.join(settings.STATICFILES_DIRS[0], 'images',
                                                                       product['img'])) else 'no-image.png'
    return product


def home(request):
    all_products = Product.objects.all()
    num_products = min(6, len(all_products))
    if request.user.is_authenticated:
        user = request.user
        product_ids = Cart.objects.filter(customer=user).values_list('product__id', flat=True)
    else:
        product_ids = []
    return render(request, 'app/home.html', {
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'products': random.sample(list(all_products), num_products),
        'products_in_cart': product_ids
    })


def product(request, slug):
    if request.user.is_authenticated:
        user = request.user
        product_ids = Cart.objects.filter(customer=user).values_list('product__id', flat=True)
    else:
        product_ids = []

    return HttpResponse(render(request, 'app/product.html', {
        'product': Product.objects.get(slug=slug),
        'products_in_cart': product_ids
    }))


def category(request, slug):
    subcategory = Subcategory.objects.get(slug=slug)
    if request.user.is_authenticated:
        user = request.user
        product_ids = Cart.objects.filter(customer=user).values_list('product__id', flat=True)
    else:
        product_ids = []

    return HttpResponse(render(request, 'app/products.html', {
        'products': Product.objects.filter(subcategory=subcategory),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'category': subcategory,
        'products_in_cart': product_ids
    }))


def cart(request):
    if request.user.is_authenticated:
        user = request.user
        return HttpResponse(render(request, 'app/cart.html', {
            'cart': Cart.objects.filter(customer=user),
            'total_price': totalPrice(user)
        }))
    else:
        return redirect('home')


def search(request, query):
    if request.user.is_authenticated:
        user = request.user
        product_ids = Cart.objects.filter(customer=user).values_list('product__id', flat=True)
    else:
        product_ids = []

    return HttpResponse(render(request, 'app/products.html', {
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'products': Product.objects.filter(title__icontains=query),
        'search': query,
        'products_in_cart': product_ids
    }))


@login_required
def profile(request):
    user = request.user
    return HttpResponse(render(request, 'accounts/profile.html', {
        'profile': user
    }))
