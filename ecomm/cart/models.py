from django.db import models
from products.models import Product
from user.models import UserBase
from django.core.validators import MinValueValidator


class Cart (models.Model):
    user     = models.ForeignKey(UserBase, on_delete=models.CASCADE)
   
    
    def __str__(self):
        return self.user.username
    
class CartItems (models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return self.product.name
