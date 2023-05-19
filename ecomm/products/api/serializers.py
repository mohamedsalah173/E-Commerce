from rest_framework import serializers
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from categories.api.serializers import categoriesSerializers
from categories.models import Categories
def validate_name(value):
    if not value:
        raise serializers.ValidationError("Name cannot be empty")
    if not str(value).isalnum():
        raise serializers.ValidationError("Name must only contain letters and numbers")
    if len(value) < 3:
        raise serializers.ValidationError("Name must be at least 3 characters long")

def validate_description(value, name):
    if len(value) < 10:
        raise serializers.ValidationError("Description must be at least 10 characters long")
    if value == name:
        raise serializers.ValidationError("Description must be different from name")
    
def validate_image(value):
    if not value.content_type.startswith('image'):
        raise serializers.ValidationError("Image must be of type image/*")
        
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(max_length=None,allow_empty_file=False,allow_null=True)
    name = serializers.CharField(max_length=50, required=True, validators=[validate_name],allow_null=False)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=11, decimal_places=2, required=True, validators=[MinValueValidator(0),MaxValueValidator(1000000000)])
    is_active = serializers.BooleanField(required=False)
    # categories = categoriesSerializers()
    # categories = serializers.PrimaryKeyRelatedField(queryset=Categories.objects.all(), many=False)
    category_name = serializers.SerializerMethodField()

    def get_category_name(self, obj):
        return obj.categories.name
    
    url = serializers.HyperlinkedIdentityField(
        view_name='productDetailAV',
        lookup_field='pk'
    )
    
    def validate(self, data):
        if 'name' in data and 'description' in data:
            validate_description(data['description'], data['name'])
        data['is_active'] = data.get('stoke', 0) > 0
        return data
    
    class Meta:
        model = Product
        fields = '__all__'
        
        
        
        
        
 