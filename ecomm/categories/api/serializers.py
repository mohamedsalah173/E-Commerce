from rest_framework import serializers
from categories.models import Categories

class categoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
        
    def create(self,validated_data) :
        return Categories.objects.create(**validated_data)
    
    def update(self,instance,validated_data) :
        if instance.name :
         instance.name = validated_data.get('name',instance.name)
        if instance.description :
         instance.description = validated_data.get('description',instance.description)
        instance.save()
        return instance   
