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

from .models import Task
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer
)
from .filters import TaskFilter
from django.http import HttpResponse


from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

#Websocket imports
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


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
            
            
            #Use websockets to notify cottage owners of new task
            channel_layer = get_channel_layer()
            if request.user.access_to_cottage.owner.id and request.user.access_to_cottage.owner and serializer.data:
                group_name = f"tasks_group_{str(request.user.access_to_cottage.id)}"
                async_to_sync(channel_layer.group_send)(
                    group_name, # This must match the room name in consumers.py
                    {    
                        'type': 'task_message', # This calls the method in your Consumer
                        'data': serializer.data
                    }
                )
                print("Task websocket message sent to group:", group_name)
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

        #Use websockets to notify cottage owners of new task
        channel_layer = get_channel_layer()
        if request.user.access_to_cottage.owner.id and request.user.access_to_cottage.owner and serializer.data:
            group_name = f"tasks_group_{str(request.user.access_to_cottage.id)}"
            async_to_sync(channel_layer.group_send)(
                group_name, # This must match the room name in consumers.py
                {    
                    'type': 'task_message', # This calls the method in your Consumer
                    'data': serializer.data
                }
            )
            print("Task websocket message sent to group:", group_name)

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
