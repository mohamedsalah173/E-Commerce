from products.models import Product
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.decorators import APIView
from products.api.serializers import ProductSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser


class productListAV(APIView):

    def get(self, request):
        permission_classes = [AllowAny]
        products = Product.objects.all()
        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        permission_classes = [IsAdminUser]
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class productDetailAV(APIView):

    def get(self, request, pk):
        permission_classes = [AllowAny]
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        permission_classes = [IsAdminUser]
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
        permission_classes = [IsAdminUser]
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
