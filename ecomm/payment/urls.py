from django.urls import path

from .views import StripeCheckOutView

# urlpatterns = [
#     path('gettoken/<str:id>/<str:token>',views.generate_token,name='generate.token'),
#     path('process/<str:id>/<str:token>',views.payment_method,name='payment.token'),
# ]
# 
urlpatterns = [
    path('create-checkout-session',StripeCheckOutView.as_view(),name='StripeCheckOutView'),
]
    