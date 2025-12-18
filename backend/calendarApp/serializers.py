from rest_framework import serializers
from .models import Reservation
from django.contrib.auth import authenticate



class ReservationSerializer(serializers.ModelSerializer):
    eventColor = serializers.CharField(source='reservationOwner.user_color', read_only=True)
    ownerName = serializers.CharField(source='reservationOwner.username', read_only=True)
    class Meta:
        model = Reservation

        fields = [
                    'title', 'start', 'end', 'description', 'owner', 'id', 'eventColor', 'ownerName', 'reservationOwner'
                ]