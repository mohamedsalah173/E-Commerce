from django.urls import path, include
# from products.api.views import product_list ,product_details
from products.api.views import productListAV, productDetailAV
from rest_framework.permissions import IsAuthenticatedOrReadOnly
urlpatterns = [
    path('list/', productListAV.as_view(),
         permission_classes=[IsAuthenticatedOrReadOnly]),
    path('<int:pk>/', productDetailAV.as_view(), name='productDetailAV',
         permission_classes=[IsAuthenticatedOrReadOnly]),
]
