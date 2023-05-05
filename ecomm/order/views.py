from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# from user.models import User
from .models import Order
from .serializers import OrderSerializers

class AllOrder(APIView):
    
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializers(orders, many=True)
        return Response(serializer.data)

class AddOrder(APIView):
    
    # def validateUser(self, id):
    #     try:
    #         user = User.objects.get(id=id)
    #     except User.DoesNotExist:
    #         return None
    #     return user
        
    def post(self, request):
        # id=request.data.get('id')
        # user = self.validateUser(id)
        # if user is None:
        #     return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetailed(APIView):
    
    def get(self, request, id):
        try:
            order = Order.objects.get(id=id)
        except order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        serializer = OrderSerializers(order)
        return Response(serializer.data)

    def put(self, request, id):
        order=Order.objects.get(id=id)
        serializer = OrderSerializers(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        order=Order.objects.get(id=id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)