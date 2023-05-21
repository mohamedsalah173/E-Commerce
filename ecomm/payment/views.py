import stripe
from django.conf import settings
from rest_framework import status
from django.shortcuts import  redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from order.views import OrderItemsList, OrderChanges;
from rest_framework.permissions import IsAdminUser ,IsAuthenticated
from cart.models import Cart, CartItems
from user.models import UserBase
import json


stripe.api_key = settings.STRIP_SECRETE_KEY

class StripeCheckOutView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        base_url = request.scheme + '://' + request.get_host()
        user= self.request.GET.get('user')
        # user_id = user_info.get('user_id')
        print(user)
        print('------------')
        cart = Cart.objects.get(user=user)
        print(cart)
        cart_items = CartItems.objects.filter(cart=cart)
        line_items = []
        for item in cart_items:
            product_name = item.product.name
            price = item.product.price * 100  # Stripe requires the price in cents
            line_item = {
                'price_data' :{
                    'currency' : 'usd',  
                    'product_data': {
                        'name': product_name,
                    },
                    'unit_amount': int(price)
                },
                'quantity' : item.quantity
            }
            line_items.append(line_item)
        try:                
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                # success_url=settings.SITE_URL + '/?success=true/' + 'session_id={CHECKOUT_SESSION_ID}',
                success_url=base_url + f'/order/add-item?user={user}',
                cancel_url=base_url  + '?canceled=true',
                
            )
            return redirect(checkout_session.url)
        except:
            return Response(
                {'error':'some thing went wrong while session checkout id'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )