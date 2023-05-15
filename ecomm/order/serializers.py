from rest_framework import serializers
from user.models import UserBase
from .models import Order, OrderItems



class OrderItemsSerializers(serializers.ModelSerializer):
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = OrderItems
        exclude=['order']

        
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value
     
class OrderSerializers(serializers.ModelSerializer):

    items = OrderItemsSerializers(many=True, required=False)
    total_amount = serializers.SerializerMethodField()
    user = UserBase()

    class Meta:
        model = Order
        fields = '__all__'
    
    def get_total_amount(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.product.price * item.quantity
        return total