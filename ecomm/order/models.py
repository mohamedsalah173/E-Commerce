from django.db import models
# from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from products.models import Product
from user.models import UserBase
import uuid


def validate_product_name(value):
    if len(value) < 3:
        raise ValidationError('Product name must be at least 3 characters long.')

SHIPPING_STATUS = [
    ('P', 'Pending'),
    ('S', 'Shipped'),
    ('D', 'Delivered'),
]

class Order(models.Model):

    transaction_id= models.UUIDField(default=uuid.uuid4, editable=False)
    shipping = models.CharField(max_length=1, choices=SHIPPING_STATUS ,default='P', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE, null=True);

    def __str__(self):
        return self.shipping + ' -- ' + str(self.transaction_id)
    

        
class OrderItems(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveBigIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='items')
    
    def __str__(self):
        return self.product.name + ' -- ' + str(self.product.price * self.quantity)
    
    def get_item_price(self):
        return self.product.price * self.quantity
    