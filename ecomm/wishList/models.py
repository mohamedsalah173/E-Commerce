from django.db import models
from products.models import Product
from user.models import UserBase
import uuid
class WishList(models.Model):
    user_id = models.ForeignKey(UserBase, on_delete=models.DO_NOTHING,null=True)
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING,null=True)
# Create your models here.
