from django.urls import path
from .views import order_list, order_item_details

urlpatterns = [
    path('allorder/', order_list, name="allorder"),
    path('orderdetails/<int:id>/', order_item_details, name="orderdetails"),
]
    