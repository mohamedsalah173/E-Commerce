from django.urls import path, include
# from products.api.views import product_list ,product_details
from products.api.views import productListAV, productDetailAV
from rest_framework.permissions import IsAuthenticatedOrReadOnly
urlpatterns = [
    path('list/', productListAV.as_view()
         ),
    path('<int:pk>/', productDetailAV.as_view(), name='productDetailAV'
         ),
]
