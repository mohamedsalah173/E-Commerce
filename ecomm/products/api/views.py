from products.models import Product
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.decorators import APIView
from products.api.serializers import ProductSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.utils.urls import replace_query_param
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

class productListAV(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LimitOffsetPagination
    
    def get(self, request,*args, **kwargs):
       return self.list(request, *args, **kwargs)
  
    def post(self, request):
        
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return super().get_permissions()

#  cruds  for one  product 
class productDetailAV(APIView):

    def get(self, request, pk):
       
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
       
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product updated successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
    
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    def get_permissions(self):
        if self.request.method in ['PUT','DELETE']:
            return [IsAdminUser()]
        return super().get_permissions()