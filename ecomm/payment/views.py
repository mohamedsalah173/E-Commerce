# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse, JsonResponse
# from django.contrib.auth import get_user_model
# from django.views.decorators.csrf import csrf_exempt
# import braintree


# # Create your views here.

# gateway = braintree.BraintreeGateway(
#     braintree.Configuration(
#         braintree.Environment.Sandbox,
#         merchant_id="8kwh5rb3nzygncb3",
#         public_key="mxzkmfs7qcn55vhv",
#         private_key="78bf25be968fc4ecd7c30f6111fd8fd0"
#     )
# )

# def validate_user_session(id, token):
#     UserModel = get_user_model()
#     try:
#         user = UserModel.objects.get(pk=id)
#         if user.session_token == token:
#             return True
#     except:
#         if UserModel.DoesNotExist():
#             return False

# @csrf_exempt
# def generate_token(request, id, token):
#     if not validate_user_session(id, token):
#         JsonResponse({'error':'you must login again please !'})
        
#     return JsonResponse({'client_token':gateway.client_token.generate(), 'success':True})

# @csrf_exempt
# def payment_method(request, id, token):
#     if not validate_user_session(id, token):
#         JsonResponse({'error':'you must login again please !'})
        
#     nonce_from_the_client = request.POST['paymentMethodNonce']
#     amount_from_the_client = request.POST['paymentMethodNonce']
    
#     result = gateway.transaction.sale({
#     "amount": amount_from_the_client,
#     "payment_method_nonce": nonce_from_the_client,
#     "options": {
#       "submit_for_settlement": True
#     }
#     })
    
#     if result.is_succes:
#         return JsonResponse({
#             'success':result.is_success,
#             'transaction':{
#                 'id':result.transaction.id,
#                 'amount':result.transaction.amount,
#             }
#             })
#     else:
#         JsonResponse({'error':True, 'success':False})
#! /usr/bin/env python3.6


import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51N6ijoDIajLiykdANbBTjryP0yU2fqkf3Ta8vB4LepConqUjHImukXhzXsFFTgs0iOTmH9BSZb7Y25mMTT59oysA00UfbdvZGQ'

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:4242'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': '{{PRICE_ID}}',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '?success=true',
            cancel_url=YOUR_DOMAIN + '?canceled=true',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

if __name__ == '__main__':
    app.run(port=4242)