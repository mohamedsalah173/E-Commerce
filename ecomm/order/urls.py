from django.urls import path
from .views import AllOrder, OrderDetailed, AddOrder
from rest_framework.permissions import IsAuthenticated
urlpatterns = [
    path('allorder/', AllOrder.as_view(), name="allorder",
         permission_classes=[IsAuthenticated]),
    path('add/<int:id>/', AddOrder.as_view(), name='addOrder',
         permission_classes=[IsAuthenticated]),
    path('orderdetails/<int:id>/', OrderDetailed.as_view(),
         name="orderdetails", permission_classes=[IsAuthenticated]),
]
