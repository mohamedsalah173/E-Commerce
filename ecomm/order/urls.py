from django.urls import path
from .views import AllOrder, OrderDetailed, AddOrder

urlpatterns = [
    path('allorder/', AllOrder.as_view(), name="allorder"),
    path('add/<int:id>/', AddOrder.as_view(), name='addOrder'),
    path('orderdetails/<int:id>/', OrderDetailed.as_view(), name="orderdetails"),
]