from django.shortcuts import render
from django.http import JsonResponse
from .serializers import cartSerializers ,cartItemsSerializers
from .models import Cart , CartItems
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated 



@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser, IsAuthenticated])
def addToCart(request):
    print(request.data)
    serializer = cartSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        return JsonResponse({'data': data})
    else:
        return Response(serializer.errors)



@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser, IsAuthenticated])
def addToCartItems(request):
    print(request.data)
    serializer = cartItemsSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        return JsonResponse({'data': data})
    else:
        return Response(serializer.errors)
    
    
@api_view(['GET'])
def getAllCartItems(request):
    try:
        cartitems = CartItems.objects.all()
    except CartItems.DoesNotExist:
        return Response("notfound")
    serializer = cartItemsSerializers(cartitems, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getAllCart(request):
    try:
       cart =Cart.objects.all()
    except Cart.DoesNotExist:
        return Response("notfound")
    serializer = cartSerializers(cart, many=True)
    return Response(serializer.data)

@api_view(['GET','DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def getCartById(request, id):
    try:
        cart = Cart.objects.get(id=id)
    except Cart.DoesNotExist:
        return Response("notfound")
    if request.method == 'GET':
        serializer = cartSerializers(cart)
        return JsonResponse(serializer.data)
   
                    
    if request.method == 'DELETE':
          try:
             cart.delete()
             return Response("Deleted")
             
          except:
             return Response(category.errors)
        

    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser | IsAuthenticated])
def getCartItemsById(request, id):
    try:
        cartitems = CartItems.objects.get(id=id)
    except CartItems.DoesNotExist:
        return Response("notfound")
    if request.method == 'GET':
        permission_classes = [AllowAny]
        serializer = cartItemsSerializers(cartitems)
        return JsonResponse(serializer.data)
    #  if request.method == 'PUT':
        
        # try:
        #     cart = Cart.objects.get(id=id)
        # except Cart.DoesNotExist:
        #     return Response("notfound")

        # serializer = cartSerializers(cart, data=request.data, partial=True)
        # if serializer.is_valid():
        
        #     if 'products' in request.data:
        #         cart.products = request.data['products']
        #         print(cart.products)
        #     if 'user' in request.data:
        #         cart.user = request.data['user']
                
        #     cart.save()
        #     return Response(serializer.data)
        # else:    
        #     return Response(serializer.errors)
                
                
                    
    if request.method == 'DELETE':
          try:
             cartitems.delete()
             return Response("Deleted")
             
          except:
             return Response(cartitems.errors)
            

   
    
    
    