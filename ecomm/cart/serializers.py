from rest_framework import serializers
from cart.models import Cart 
from  .models  import CartItems 
from user.serializer import LoginSerializer
# from products.api.serializers import ProductSerializer
from user.models import UserBase
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class cartSerializers(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'
        
    def create(self, validated_data):
        return Cart.objects.create(**validated_data)
    
     
    
class cartItemsSerializers(serializers.ModelSerializer):
    product = ProductSerializer()
  
    class Meta:
        model = CartItems
        fields = '__all__'
        
    def create(self, validated_data):
        return CartItems.objects.create(**validated_data) 
    
    def update(self,instance,validated_data) :
        if instance.user :
         instance.user = validated_data.get('user',instance.user)
        if instance.products :
         instance.products = validated_data.get('products',instance.products)
        instance.save()
        return instance   
    
   