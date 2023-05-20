
from django.db import models
from products.models import Product
from user.models import UserBase

class WishLists(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.DO_NOTHING,null=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING,null=True)
    
    class Meta:
        db_table = 'wishLists'
# Create your models here.
