from django.urls import path
from .views import add_to_cart, countProductsInCart, removeFromCart, updateCountFromCart, checkout
from accounts.views import update_profile

urlpatterns = [
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('get-count-products/in-cart/', countProductsInCart),
    path('remove-from-cart/', removeFromCart),
    path('update-count-from-cart/', updateCountFromCart),
    path('checkout/', checkout),
    path('update_profile/', update_profile),
]
