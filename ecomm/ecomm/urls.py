from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
        path('order/', include('order.urls')),

    path('product/', include('products.api.urls')),
]
