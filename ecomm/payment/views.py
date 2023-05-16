import stripe
from django.conf import settings
from rest_framework import status
from django.shortcuts import  redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from order.views import OrderItemsList;


stripe.api_key = settings.STRIP_SECRETE_KEY

class StripeCheckOutView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            order_id = 123  # Replace with the actual order ID
            response = request.get(f'{settings.SITE_URL}/order/{order_id}')
            
            if response.status_code == status.HTTP_200_OK:
                order_data = response.json()
                order_price = order_data['price']
                order_name = order_data['name']
                order_image = order_data['image']
            else:
                return Response({'error': 'Failed to retrieve order details'}, status=response.status_code)
            checkout_session = stripe.checkout.Session.create(
                
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': int(order_price) * 100,
                            'product_data': {
                                'name': order_name,
                                'images': [order_image],
                            },
                        },
                        'quantity': 1,
                    },        
                ],
                # payment_method_types=['card'],
                mode='payment',
                # success_url=settings.SITE_URL + '/?success=true/' + 'session_id={CHECKOUT_SESSION_ID}',
                success_url=settings.SITE_URL + '/order',
                cancel_url=settings.SITE_URL  + '?canceled=true',
                
            )
            return redirect(checkout_session.url)
        except:
            return Response(
                {'error':'some thing went wrong while session checkout id'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
