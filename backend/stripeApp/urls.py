from django.urls import path
from .views import create_payment_link, stripe_webhook, update_user_plan
from django.urls import path

urlpatterns = [
    #path('create-paymentlink/<str:plan>/<str:email>/', create_payment_link),
    path('stripe-webhook/', stripe_webhook),
    path('test-update/', update_user_plan),
]
