from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.db.models import Count, Q
from django.utils import timezone
from django.http import HttpResponse
from django.http import JsonResponse

from datetime import timedelta

from .models import Task
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer
)
from .filters import TaskFilter



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['name', 'location', 'month_correlation']
    ordering_fields = ['name', 'created_at', 'updated_at', 'status']
    ordering = ['-created_at']
    


    
    def get_queryset(self):
        if self.request.user.access_to_cottage:
            return Task.objects.filter(owner=self.request.user.access_to_cottage)

        else:
            return Task.objects.none()  
        
    def create(self, request, *args, **kwargs):
        if request.user.access_to_cottage:
            serializer = TaskCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user.access_to_cottage)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        return Response({'status': 'failed'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Force Responsible_for_the_task to be request.user
        instance.Responsible_for_the_task = request.user
        
        # Update other fields from request.data if any
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_done(self, request, pk=None):
        task_instance = self.get_object()
        if not task_instance:
            return Response({'error': 'No task found.'}, status=status.HTTP_400_BAD_REQUEST)
        
        #Remove note from JSON
        task_instance.status = "done"
        task_instance.Responsible_for_the_task = request.user
        task_instance.save()
        return Response({'status': 'Task status updated'}, status=status.HTTP_200_OK)
