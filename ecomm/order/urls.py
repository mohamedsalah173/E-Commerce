from django.urls import path
from .views import OrderList, OrderItemDetail, AddOrder, OrderChanges, AddOrderItem, OrderItemsList
# from rest_framework.permissions import IsAuthenticated
urlpatterns = [
    path('', OrderList.as_view(), name="orderList"), #--> done
    path('<int:pk>/', OrderItemsList.as_view(), name='orderitemslist'), #--> done
    path('add/', AddOrder.as_view(), name='addOrder'), #--> done
    path('add/item/<int:pk>/', AddOrderItem.as_view(), name='additem'), #--> done
    path('<int:pk>/item/<int:id>/', OrderChanges.as_view(), name="orderchanges"),
    path('<int:pk>/details/<int:item>/', OrderItemDetail.as_view(), name="orderdetails"), #--> done
]


#   path('', OrderList.as_view(), name="orderList"), #--> done
#     path('<int:pk>/', OrderItemsList.as_view(), name='orderitemslist'), #--> done
#     path('additems/', AddItems.as_view(), name='additems'), #--> done
#     path('<int:pk>/item/<int:id>/', OrderChanges.as_view(), name="orderchanges"), #--> done 
#     path('items/<int:item>/', OrderItemDetail.as_view(), name="orderdetails"), #--> done
#     # path('add/', AddOrder.as_view(), name='addOrder'), #--> done
