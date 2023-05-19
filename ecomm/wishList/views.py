from django.http import JsonResponse
from .serializers import wishListSerializers
from .models import WishList
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated

# @permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['POST', 'GET'])
def add_wishListItem(request):
    print(request.data)
    serializer = wishListSerializers(data=request.data)
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
        wishlist = WishList.objects.get(id=id)
    except WishList.DoesNotExist:
        return Response("notfound")
    if request.method == 'GET':
        permission_classes = [AllowAny]
        serializer = wishListSerializers(wishlist)
        return JsonResponse(serializer.data)
                  
    if request.method == 'DELETE':
          try:
             wishlist.delete()
             return Response("Deleted")
             
          except:
             return Response(wishlist.errors)
            
# @permission_classes([IsAdminUser, IsAuthenticated])
# @api_view(['GET', 'DELETE'])
# def getwishItemByUserId(request, user_id):
   
#     try:
#         wishlists = WishList.objects.filter(user_id=user_id)
#     except WishList.DoesNotExist:
#         return Response("notfound")
#     if request.method == 'GET':
#         serializer = wishListSerializers(wishlists, many=True)
#         return Response(serializer.data)
                  
#     if request.method == 'DELETE':
#           try:
#              wishlists.delete()
#              return Response("Deleted")
             
#           except:
#              return Response(wishlists.errors)   

# @permission_classes([IsAdminUser, IsAuthenticated])
# @api_view(['GET', 'DELETE'])
# def getwishItemByProductId(request, product_id):
   
#     try:
#         wishlists = WishList.objects.filter(product_id = product_id)
#     except WishList.DoesNotExist:
#         return Response("notfound")
#     if request.method == 'GET':
#         serializer = wishListSerializers(wishlists, many=True)
#         return Response(serializer.data)
                  
#     if request.method == 'DELETE':
#           try:
#              wishlists.delete()
#              return Response("Deleted")
             
#           except:
#              return Response(wishlists.errors)   


# @permission_classes([IsAdminUser, IsAuthenticated])
@api_view(['GET'])
def getAllwishList(request):   
    try:
        wishlist =WishList.objects.all()
    except WishList.DoesNotExist:
        return Response("notfound")
    serializer = wishListSerializers(wishlist, many=True)
    return Response(serializer.data)
