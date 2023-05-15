from django.urls import path
from .api import views


urlpatterns = [

    path('addcategory', views.add_category),
    path('getAllCategories', views.getAllCategories
         ),
    path('getCategoryById/<int:id>', views.getCategoryById
         )

]
