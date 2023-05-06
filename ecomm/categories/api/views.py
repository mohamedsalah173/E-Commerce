from django.http import JsonResponse
from .serializers import categoriesSerializers
from categories.models import Categories
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated


@api_view(['POST', 'GET'])
def add_category(request):

    serializer = categoriesSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        return JsonResponse({'data': data})
    else:
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def getCategoryById(request, id):
    try:
        category = Categories.objects.get(id=id)
    except Categories.DoesNotExist:
        return Response("notfound")
    if request.method == 'GET':
        permission_classes = [AllowAny]
        serializer = categoriesSerializers(category)
        return JsonResponse(serializer.data)
    if request.method == 'PUT':
        permission_classes = [IsAdminUser]
        serializer = categoriesSerializers(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors)

    if request.method == 'DELETE':
        permission_classes = [IsAdminUser]
        try:
            category.delete()
            return Response("Deleted")

        except:
            return Response(category.errors)


@api_view(['GET'])
def getAllCategories(request):
    permission_classes = [AllowAny]
    try:
        category = Categories.objects.all()
    except Categories.DoesNotExist:
        return Response("notfound")
    serializer = categoriesSerializers(category, many=True)
    return Response(serializer.data)
