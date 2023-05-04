from rest_framework import serializers
from .models import Order, SHIPPING_STATUS


class OrderSerializers(serializers.Serializer):
    
    id = serializers.IntegerField(read_only=True)
    product_name = serializers.CharField()
    quantity = serializers.IntegerField()
    shipping = serializers.ChoiceField(choices=SHIPPING_STATUS)
    transaction_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    
    def create(self, validated_data):
        return Order.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.product_name = validated_data.get("product_name", validated_data.product_name)
        instance.quantity = validated_data.get("quantity", validated_data.quantity)
        instance.shipping = validated_data.get("shipping", validated_data.shipping)
        instance.transaction_id = validated_data.get("transaction_id", validated_data.transaction_id)
        instance.updated_at = validated_data.get("updated_at", validated_data.updated_at)
        instance.save()
        return instance