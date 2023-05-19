from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status, generics
from rest_framework import serializers
from django.db.models import F, Sum
from .models import Order, OrderItems
from .serializers import OrderSerializers, OrderItemsSerializers
from cart.models import Cart, CartItems
# from django.core.exceptions import ValidationError



class OrderList(generics.ListAPIView):
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
    serializer_class = OrderSerializers
    
    def get_queryset(self):
        return Order.objects.all()

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        total_price = 0
        cart_items = cart.items.all()
        for cart_item in cart_items:
            item_total = cart_item.product.price * cart_item.quantity
            total_price += item_total
            
        # Create an order
        order = Order(user=request.user, status='Pending', total_price=total_price)
        order.save()

        # Retrieve cart items and add them to the order
        cart_items = cart.products.all()
        for cart_item in cart_items:
            order_item = OrderItems(product=cart_item.product, quantity=cart_item.quantity, order=order)
            order_item.save()

            # Update the product stoke
            product = cart_item.product
            product.stoke -= cart_item.quantity
            product.save()

        # Clear the cart
        cart.items.all().delete()

        serializer = OrderSerializers(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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