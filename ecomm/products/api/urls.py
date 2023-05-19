from django.urls import path, include
from products.api.views import productListAV, productDetailAV

urlpatterns = [
    path('', productListAV.as_view()),
    path('<int:pk>', productDetailAV.as_view(), name='productDetailAV'),
]
