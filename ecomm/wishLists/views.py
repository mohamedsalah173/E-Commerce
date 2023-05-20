from django.shortcuts import render
from django.http import JsonResponse
from .serializer import wishListsSerializers
from .models import WishLists
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated


@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET'])
def getAllwishList(request):   
    try:
        wishlist =WishLists.objects.all()
    except WishLists.DoesNotExist:
        return Response("notfound")
    serializer = wishListsSerializers(wishlist, many=True)
    return Response(serializer.data)


@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['POST', 'GET'])
def add_wishListItem(request):
    print(request.data)
    serializer = wishListsSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        return JsonResponse({'data': data})
    else:
        return Response(serializer.errors)
    
@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def getwishItemById(request, id):
    permission_classes = [IsAdminUser|IsAuthenticated]
    try:
        wishlist = WishLists.objects.get(id=id)
    except WishList.DoesNotExist:
        return Response("notfound")
    if request.method == 'GET':
        permission_classes = [AllowAny]
        serializer = wishListsSerializers(wishlist)
        return JsonResponse(serializer.data)
                  
    if request.method == 'DELETE':
          try:
             wishlist.delete()
             return Response("Deleted")
             
          except:
             return Response(wishlist.errors)


@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET', 'DELETE'])
def getwishItemByUserId(request, user):
   
    try:
        wishlists = WishLists.objects.filter(user=user)
    except WishList.DoesNotExist:
        return Response("notfound")
    if request.method == 'GET':
        serializer = wishListsSerializers(wishlists, many=True)
        return Response(serializer.data)
                  
    if request.method == 'DELETE':
          try:
             wishlists.delete()
             return Response("Deleted")
             
          except:
             return Response(wishlists.errors)   
         
         
         
@permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET', 'DELETE'])
def getwishItemByProductId(request, product):
   
    try:
        wishlists = WishLists.objects.filter(product = product)
    except WishList.DoesNotExist:
        return Response("notfound")
    if request.method == 'GET':
        serializer = wishListsSerializers(wishlists, many=True)
        return Response(serializer.data)
                  
    if request.method == 'DELETE':
          try:
             wishlists.delete()
             return Response("Deleted")
             
          except:
             return Response(wishlists.errors)   

# Create your views here.
