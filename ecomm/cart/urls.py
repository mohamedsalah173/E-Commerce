from django.urls import path
from . import views


urlpatterns = [
   path('addToCart',views.addToCart),
   path('addToCartItems',views.addToCartItems),
   path('cart',views.getAllCart),
   path('CartItems',views.getAllCartItems),
   path('getCartById/<int:id>',views.getCartById),
   path('getCartItemsById/<int:id>',views.getCartItemsById),
   path('getCartItemsByUserId/<int:user>',views.getCartByUserId),
   path('getCartItemsByProductId/<int:product>/<int:cart>/',views.getCartItemsByProductId),
   path('getCartItemsByCartId/<int:cart>',views.getCartItemsByCartId)
]
