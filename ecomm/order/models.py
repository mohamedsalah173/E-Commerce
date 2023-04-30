from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models
# from django.db.models.signals import pre_save
# from django.dispatch import receiver
import uuid
# import datetime
# from user import models 
def validate_product_name(value):
    if len(value) < 3:
        raise ValidationError('Product name must be at least 3 characters long.')


class Order(models.Model):
    
    SHIPPING_STATUS = [
        ('P', 'Pending'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
    ]
    # user = models.ForeignKey(User, on_delete=models.CASCADE); // waiting for amany
    product_name = models.CharField(max_length=20, validators=[validate_product_name])
     
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    
    # search for transaction_id 
    transaction_id= models.IntegerField(unique=True,null=False) 
    
    shipping = models.CharField(max_length=1, choices=SHIPPING_STATUS ,default='P', null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate a random UUID and convert it to an integer
            self.transaction_id = int(uuid.uuid4().int & (10**12-1))
        super().save(*args, **kwargs)
        
