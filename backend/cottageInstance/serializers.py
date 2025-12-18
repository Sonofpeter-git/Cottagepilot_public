from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CottageInstanceModel
from django.core.exceptions import ValidationError as DjangoValidationError

class cottageSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CottageInstanceModel
        fields = ['name', 'address', 'stripe_subscription']


class CottageSerializer(serializers.ModelSerializer):
    stripe_payment_status_int = serializers.IntegerField(read_only=True)
    ownerUsername = serializers.CharField(max_length=100, read_only=True)

    class Meta:
        model = CottageInstanceModel
        fields = ['id', 'name', 'owner', 'ownerUsername', 'address', 'stripe_subscription', 'stripe_payment_status_int']


class inviteMembers(serializers.Serializer):
    email = serializers.EmailField()