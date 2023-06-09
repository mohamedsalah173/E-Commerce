from django.db import models
from django.core.validators import MinValueValidator
from categories.models import Categories
# Create your models here.
class Product(models.Model):
  categories=models.ForeignKey(Categories,on_delete=models.CASCADE,null=True)
  name =models.CharField(max_length=50,null=False,blank=False)
  description =models.TextField(null=False,blank=False)
  price=models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)])
  is_active=models.BooleanField(default=True)
  stoke=models.PositiveIntegerField()
  created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
  updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)
  image=models.ImageField(upload_to='images/%y/%m/%d',null=True,blank=True)
  
  def __str__(self):
    return self.name