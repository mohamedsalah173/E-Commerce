from rest_framework import serializers
from user.models import UserBase
from .models import Order, OrderItems



class OrderItemsSerializers(serializers.ModelSerializer):
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = OrderItems
        exclude=['order']
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=OrderItems.objects.all(),
        #         fields=('product', 'order'),
        #         message='Product already exists in this order'
        #     )
        # ]
        
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value
    
    # def validate(self, data):
    #     quantity = data.get('quantity')
    #     product = data.get('product')
    #     if quantity > product.stoke:
    #         raise serializers.ValidationError("Quantity is greater than the product's stock.")
    #     return data
        
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
    