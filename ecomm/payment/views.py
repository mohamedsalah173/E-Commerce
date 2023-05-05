from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import braintree
# Create your views here.

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="8kwh5rb3nzygncb3",
        public_key="mxzkmfs7qcn55vhv",
        private_key="78bf25be968fc4ecd7c30f6111fd8fd0"
    )
)

def validate_user_session(id, token):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
    except:
        if UserModel.DoesNotExist():
            return False

@csrf_exempt
def generate_token(request, id, token):
    if not validate_user_session(id, token):
        JsonResponse({'error':'you must login again please !'})
        
    return JsonResponse({'client_token':gateway.client_token.generate(), 'success':True})

@csrf_exempt
def payment_method(request, id, token):
    if not validate_user_session(id, token):
        JsonResponse({'error':'you must login again please !'})
        
    nonce_from_the_client = request.POST['paymentMethodNonce']
    amount_from_the_client = request.POST['paymentMethodNonce']
    
    result = gateway.transaction.sale({
    "amount": amount_from_the_client,
    "payment_method_nonce": nonce_from_the_client,
    "options": {
      "submit_for_settlement": True
    }
    })
    
    if result.is_succes:
        return JsonResponse({
            'success':result.is_success,
            'transaction':{
                'id':result.transaction.id,
                'amount':result.transaction.amount,
            }
            })
    else:
        JsonResponse({'error':True, 'success':False})
    