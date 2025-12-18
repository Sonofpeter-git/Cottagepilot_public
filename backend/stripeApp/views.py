# views.py
import stripe
import json
import os
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from dataclasses import dataclass
from cottageInstance.models import CottageInstanceModel

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY

@dataclass
class StripePlan:
    priceId: str
    productId: str
    planName: str
    redirect: str
    cancel_url: str

stripePlans = {
        'Basic': StripePlan(
            priceId=os.environ.get('STRIPE_BASIC_PRICEID'),
            productId=os.environ.get('STRIPE_BASIC_PRODID'),
            planName='Basic',
            redirect=os.environ.get('STRIPE_REDIRECT'),
            cancel_url=os.environ.get('STRIPE_CANCEL_URL')
        ),
        'Standard': StripePlan(
            priceId=os.environ.get('STRIPE_STANDARD_PRICEID'),
            productId=os.environ.get('STRIPE_STANDARD_PRODID'),
            planName='Standard',
            redirect=os.environ.get('STRIPE_REDIRECT'),
            cancel_url=os.environ.get('STRIPE_CANCEL_URL')
        ),
        'Standard': StripePlan(
            priceId=os.environ.get('STRIPE_PREMIUM_PRICEID'),
            productId=os.environ.get('STRIPE_PREMIUM_PRODID'),
            planName='Standard',
            redirect=os.environ.get('STRIPE_REDIRECT'),
            cancel_url=os.environ.get('STRIPE_CANCEL_URL')
        )
        }

def create_payment_link(request, plan, email):
   # stripePriceIdList = [os.environ.get("stripePriceIdList",  cast=lambda v: [s.strip() for s in v.split(',')])]
    if request.method == 'GET':
        try:
            payment_link = make_stripe_checkout_session(plan, email)
            user = request.user
            user.stripe_subscription = plan
            user.save()
            return JsonResponse({'url': payment_link})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Wrong method'}, status=405 )


#generate payment link
def make_stripe_checkout_session(plan, email):
    stripePlan = stripePlans[plan]
    session = stripe.checkout.Session.create(
        line_items=[{
            'price': stripePlan.priceId ,
            'quantity': 1,
        }],
        mode='subscription',  # or 'payment' if it's a one-time charge
        success_url=stripePlan.redirect,
        cancel_url=stripePlan.cancel_url,
        customer_email=email 
    )
    return session.url

def update_user_plan(cus_id, user):
    try:
        # List all subscriptions for the customer
        subscriptions = stripe.Subscription.list(customer=cus_id, limit=10)

        results = []

        for sub in subscriptions.auto_paging_iter():
            items = [
                {
                    'id': item.id,
                    'price_id': item.price.id,
                    'product': item.price.product,
                    'unit_amount': item.price.unit_amount,
                    'currency': item.price.currency,
                }
                for item in sub['items']['data']
            ]

            results.append({
                'subscription_id': sub.id,
                'status': sub.status,
                'items': items,
            })

            prod_id = results[0]['items'][0]['product']
            # Find the matching plan name
            plan_name = next((plan.planName for plan in stripePlans.values() if plan.productId == prod_id), None)
            user.stripe_subscription = plan_name
            user.save()




    except stripe.error.InvalidRequestError as e:
        return {'error': str(e)}
                 


from django.http import HttpResponse, HttpResponseNotAllowed

@csrf_exempt
def stripe_webhook(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(['POST'])
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=webhook_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return HttpResponse(status=400)

    # Handle different event types
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Optional: retrieve customer email
        customer_email = session.get('customer_details', {}).get('email')
        payment_status = session.get('payment_status')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')
        if customer_email and payment_status == 'paid':
            try:
                user = User.objects.get(email=customer_email)
                cottageInstance = CottageInstanceModel.objects.filter(owner=user, stripe_payment_status=False).first()
                if cottageInstance:
                    user.access_to_cottage = cottageInstance
                    cottageInstance.stripe_payment_status = True
                    cottageInstance.stripe_customer_id = stripe_customer_id
                    cottageInstance.stripe_subscription_id = stripe_subscription_id
                    cottageInstance.save()
                    
                    update_user_plan(session.get('customer'), user)

            except User.DoesNotExist:
                return HttpResponse(message=f'No cottageInstance found user:{user}', status=404)

    elif event['type'] == 'payment_link.created':
        # Optional: log or notify about link creation
        link = event['data']['object']
        print("New Payment Link:", link['url'])

    elif event['type'] == 'payment_link.completed':
        # This event fires when a user completes a payment via a Payment Link
        print("Payment Link completed")

    # Handle other events as needed:
    # - 'customer.subscription.created'
    # - 'invoice.payment_succeeded'
    # - etc.

    return HttpResponse(status=200)