from django.contrib import admin
from .models import Cart
from .models import CartItems
# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItems)

