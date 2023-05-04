from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.
class Product(models.Model):
#   category=models.ForeignKey(Categories,on_delete=models.SET_NULL,null=True)
  name =models.CharField(max_length=50,null=True,blank=True)
  description =models.TextField(null=True,blank=True)
  price=models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)])
  is_active=models.BooleanField(default=False)
  stoke=models.PositiveIntegerField()
  created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
  updated_at=models.DateTimeField(auto_now=True,null=True,blank=True)
  image=models.ImageField(upload_to='productsPhotos/%y/%m/%d',null=True,blank=True)
  
  def __str__(self):
    return self.name
