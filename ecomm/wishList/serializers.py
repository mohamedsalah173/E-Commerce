from rest_framework import serializers
from wishList.models import WishList
from user.serializer import LoginSerializer
from products.api.serializers import ProductSerializer
from user.models import UserBase

class wishListSerializers(serializers.ModelSerializer):

    class Meta:
        model = WishList
        fields = '__all__'
        
    def create(self, validated_data):
        return WishList.objects.create(**validated_data)

# in your view or API endpoint

