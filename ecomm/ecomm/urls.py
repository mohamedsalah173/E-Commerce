from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('order/', include('order.urls')),
    path('payment/', include('payment.urls')),
    path('product/', include('products.api.urls')),
    path('user/', include('user.urls')),
    path('categories/', include('categories.urls')),
    path('cart/', include('cart.urls')),
    path('wishList/', include('wishList.urls')),
   
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
