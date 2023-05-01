from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.
class Product(models.Model):
#   Caregory=models.ForeignKey(Categories,on_delete=models.SET_NULL,null=True)
  Name =models.CharField(max_length=150,null=False,blank=True)
  Description =models.TextField(null=False,blank=True)
  Price=models.DecimalField(max_digits=6,decimal_places=2,validators=[MinValueValidator(0)])
  is_active=models.BooleanField(default=False)
  Stoke=models.PositiveIntegerField()
  created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
  updated_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
  image=models.ImageField(upload_to='productsPhotos/%y/%m/%d',null=True,blank=True)

