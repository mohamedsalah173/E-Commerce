from rest_framework import serializers
from categories.models import Categories
# from products.api.serializers import ProductSerializer
class categoriesSerializers(serializers.ModelSerializer):
    # products = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = Categories
        fields = ['name','description','id']
    #   read_only_fields = ['description','name']
        
    def create(self,validated_data) :
        return Categories.objects.create(**validated_data)
    
    def update(self,instance,validated_data) :
        if instance.name :
         instance.name = validated_data.get('name',instance.name)
        if instance.description :
         instance.description = validated_data.get('description',instance.description)
        instance.save()
        return instance   
