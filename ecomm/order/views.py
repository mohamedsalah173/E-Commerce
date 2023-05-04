from rest_framework.response import Response
# from rest_framework.decorators import api_view
from .models import Order
from .serializers import OrderSerializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


@api_view()
@permission_classes((permissions.AllowAny,))
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializers(orders, many=True)
    return Response(serializer.data)

@api_view()
@permission_classes((permissions.AllowAny,))
def order_item_details(request, id):
    order = Order.objects.get(id=id)
    serializer = OrderSerializers(order)
    return Response(serializer.data)