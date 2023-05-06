from django.urls import path
from .api import views
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly

urlpatterns = [

    path('addcategory', views.add_category, permission_classes=[IsAdminUser]),
    path('getAllCategories', views.getAllCategories,
         permission_classes=[IsAuthenticatedOrReadOnly]),
    path('getCategoryById/<int:id>', views.getCategoryById,
         permission_classes=[IsAuthenticatedOrReadOnly])

]
