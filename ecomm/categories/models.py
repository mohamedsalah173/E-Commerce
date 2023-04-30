from django.db import models
class Categories (models.Model) :
      name        = models.CharField(max_length=30 ,null=False)
      description = models.TextField(max_length=150 ,null=False)
      createdAt   = models.DateField(auto_now_add=True)
      updateAt    = models.DateField(auto_now_add=True)
      
      def __str__(self):
        return self.name

# Create your models here.
