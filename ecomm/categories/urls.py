from django.urls import path
from .api import views
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

urlpatterns = [

    path('addcategory', views.add_category),
    path('getAllCategories', views.getAllCategories
         ),
    path('getCategoryById/<int:id>', views.getCategoryById
         )

]
