from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status, generics
from rest_framework import serializers
from .models import Order, OrderItems
from .serializers import OrderSerializers, OrderItemsSerializers
# from django.core.exceptions import ValidationError



class OrderList(generics.ListCreateAPIView):
    serializer_class = OrderSerializers
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Order.objects.filter(user=user)
        else:
            return Order.objects.none()

    
class AddOrder(generics.ListCreateAPIView):
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = OrderSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddOrderItem(generics.ListCreateAPIView):
    
    serializer_class = OrderItemsSerializers
    queryset = OrderItems.objects.all()

    def get_queryset(self):
        try:
            order = Order.objects.get(pk=self.kwargs['pk'])
            return order.items.all()
        except Order.DoesNotExist:
            raise NotFound("Order not found")
    
    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        order.user = request.user
        serializer = OrderItemsSerializers(data=request.data)
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            if quantity == 0:
                print(f"quantity: {quantity}")
                print(f"quantity: {product.stoke}")
                return Response({'error': 'Quantity must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
            if order.items.filter(product=product).exists():
                return Response({'error': 'Product already in order items'}, status=status.HTTP_400_BAD_REQUEST)
            
            if product.stoke==0:
                return Response({'error': 'Product stoke is 0'}, status=status.HTTP_400_BAD_REQUEST)
            
            if quantity > product.stoke:
                raise serializers.ValidationError("Quantity is greater than the product's stock.")
        
            order_item = OrderItems(product=product, quantity=quantity, order=order)
            product.stoke -= quantity
            order_item.save()
            product.save()
            serializer = OrderItemsSerializers(order_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderItemsList(APIView):
    
    def get(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializers(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk, id=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)  
        if order.items.count() > 0:
            return Response({'error': 'Can not delete Order that has many items'}, status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
class OrderChanges(APIView):

    def get(self,request, pk, id):
        try:
            order = Order.objects.get(pk=pk) 
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            order_item = OrderItems.objects.get(id=id)
        except OrderItems.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderItemsSerializers(order_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, id):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            order_item = OrderItems.objects.get(id=id)
        except OrderItems.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderItemsSerializers(order_item, data=request.data)
        if serializer.is_valid():
            original_quantity = order_item.quantity # old quantity
            print(f"original_quantity: {original_quantity}")
            new_quantity = serializer.validated_data['quantity'] # new quantity
            print(f"new_quantity: {new_quantity}")
            if new_quantity == 0:
                order_item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            if new_quantity < 0:
                return Response({'error': 'Quantity must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)  
            product = order_item.product
            order_item.quantity = original_quantity + (new_quantity - original_quantity) # update order_item quantity --> old + changes
            print(f"order_item.quantity: {order_item.quantity}")
            if order_item.quantity > (product.stoke + original_quantity):
                return Response({'error': 'Quantity is more than product stoke'}, status=status.HTTP_400_BAD_REQUEST)
            # serializer.save() # Save the updated item
            print(f"product.stoke (before): {product.stoke}")
            if order_item.quantity > original_quantity:
                product.stoke = product.stoke - (order_item.quantity - original_quantity)
                print(f"product.stoke (after): {product.stoke}")
            elif order_item.quantity < original_quantity:
                product.stoke = product.stoke + (original_quantity - order_item.quantity)
                print(f"product.stoke (after): {product.stoke}")
            product.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, id):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  
        try:
            order_item = OrderItems.objects.get(id=id)
        except OrderItems.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)      
        product = order_item.product
        quantity = order_item.quantity
        product.stoke += quantity
        product.save()
        order_item.delete()
        if order.items.count() == 0:
            order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class OrderItemDetail(generics.RetrieveAPIView):
    serializer_class = OrderItemsSerializers
    queryset = OrderItems.objects.all()

    def get_object(self):
        pk = self.kwargs.get('pk') # order
        item = self.kwargs.get('item') # only one item
        order = Order.objects.get(pk=pk, user=self.request.user)
        try:
            item = order.items.get(pk=item)
            return item
        except OrderItems.DoesNotExist :
            raise NotFound("Order item not found")