from django.urls import path
from .views import home, product, category, cart, search, profile
from accounts.views import register_view, login_view, logout_view, update_profile

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('product/<slug:slug>/', product, name='product'),
    path('category/<slug:slug>/', category, name='category'),
    path('cart/', cart, name='cart'),
    path('search/<str:query>', search, name='search'),
]
