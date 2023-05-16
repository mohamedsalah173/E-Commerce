from django.urls import path
from . import views


urlpatterns = [
   path('addToCart',views.addToCart),
   path('addToCartItems',views.addToCartItems),
   path('cart',views.getAllCart),
   path('CartItems',views.getAllCartItems),
   path('getCartById/<int:id>',views.getCartById),
   path('getCartItemsById/<int:id>',views.getCartItemsById),
]