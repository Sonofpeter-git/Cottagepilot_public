from django.urls import path
from .views import createCottageSubscription, me, sendInvitation, listOfUserCottages, selectCottage
from django.urls import path



urlpatterns = [
    path('create-cottage-subscription/', createCottageSubscription),
    path('me/', me),
    path('invitations/send/', sendInvitation),
    path('user-cottages/', listOfUserCottages),
    path('select-cottage/', selectCottage)
]
