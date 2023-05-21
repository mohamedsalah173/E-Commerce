from django.db import models
# from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from products.models import Product
from user.models import UserBase
from django.utils import timezone
from datetime import timedelta
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

    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False)
    shipping = models.CharField(choices=SHIPPING_STATUS, default='P', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE, null=True, related_name='orders')
    delivered_date = models.DateTimeField(default=timezone.now() + timedelta(days=3), editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f'{self.shipping} -- {self.transaction_id}'

    def get_status(self):
        current_date = timezone.now().date()
        if self.shipping == 'P':
            if current_date > self.created_at.date() + timedelta(days=1):
                self.shipping = 'S'
                self.save()
        return self.shipping    

        
class OrderItems(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveBigIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='items')
    
    def __str__(self):
        return self.product.name + ' -- ' + str(self.product.price * self.quantity)
    
    def get_item_price(self):
        return self.product.price * self.quantity
    