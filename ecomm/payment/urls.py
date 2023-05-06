from django.urls import path

from . import views

urlpatterns = [
    path('gettoken/<str:id>/<str:token>',
         views.generate_token, name='generate.token'),
    path('process/<str:id>/<str:token>',
         views.payment_method, name='payment.token'),
]
