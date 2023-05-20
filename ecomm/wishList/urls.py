from django.urls import path
from . import views
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

urlpatterns = [

    path('addwishListItem', views.add_wishListItem),
    path('getAllwishList', views.getAllwishList),
    path('getWishList/<int:id>', views.getwishItemById),
    path('getWishListByUserId/<int:user_id>', views.getwishItemByUserId),
    path('getWishListByProductId/<int:product_id>',views.getwishItemByProductId)
    
]