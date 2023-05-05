from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from products.models import Product
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
    
    # user = models.ForeignKey(User, on_delete=models.CASCADE); // waiting for amany
    product_name = models.CharField(max_length=256)
    quantity = models.IntegerField()
    transaction_id= models.IntegerField() 
    shipping = models.CharField(max_length=1, choices=SHIPPING_STATUS ,default='P', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # price = models.ForeignKey(Product, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.transaction_id = int(uuid.uuid4().int & (10**12-1))
        super().save(*args, **kwargs)
        