from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny

from .models import Reservation
from tasks.models import Task
from .serializers import (
    ReservationSerializer
)
from django.http import HttpResponse

from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from datetime import datetime

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CalendarViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'start', 'end']
    ordering_fields = ['name']
    ordering = ['id']
    
    def get_queryset(self):
        return Reservation.objects.filter(owner=self.request.user.access_to_cottage)
    
    def create(self, request, *args, **kwargs):
        #GET and VALIDATE data
        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #save
        newReservation = serializer.save(owner=request.user.access_to_cottage)

        #create tasks required for every reserved week
        descriptionSTR = "Remeber to clean. Function in progress to customize this text."
        end_str = serializer.data.get('end')  # this is a string like "2025-08-10T00:00:00Z"

        # Parse the string into a datetime object (handling 'Z' timezone if present)
        parsed_dt = datetime.fromisoformat(end_str.replace('Z', '+00:00'))

        # Convert to 'YYYY-MM-DD' string
        time_correlation = parsed_dt.date().isoformat()

        end_cleaning = Task.objects.create(name=f'End cleaning {newReservation.reservationOwner.username}', group="Loppusiivous", description=descriptionSTR,
                                           location=self.request.user.access_to_cottage.address, owner=self.request.user.access_to_cottage,
                                           time_correlation=time_correlation, linked_to_reservation=newReservation, Responsible_for_the_task=newReservation.reservationOwner)
        
        end_cleaning.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
