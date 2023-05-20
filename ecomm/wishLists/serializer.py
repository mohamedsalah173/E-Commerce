from rest_framework import serializers
from wishLists.models import WishLists
from user.serializer import LoginSerializer
from products.api.serializers import ProductSerializer
from user.models import UserBase

class wishListsSerializers(serializers.ModelSerializer):

    class Meta:
        model = WishLists
        fields = '__all__'
        
    def create(self, validated_data):
        return WishLists.objects.create(**validated_data)