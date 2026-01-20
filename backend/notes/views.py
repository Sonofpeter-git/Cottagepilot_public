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
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

from .serializers import NoteSerializer
from .filters import NoteFilter 
from .models import Note


#Websocket imports
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_class = NoteFilter
    search_fields = ['noteClassName', 'id']
    def get_queryset(self):
        if self.request.user.access_to_cottage:
            return Note.objects.filter(owner=self.request.user.access_to_cottage).order_by('-id')
        else:
            return Note.objects.none()

    def perform_create(self, serializer):
        if self.request.user.access_to_cottage:
            serializer.save(owner=self.request.user.access_to_cottage)

            #Use websockets to notify cottage owners of new task
        channel_layer = get_channel_layer()
        if self.request.user.access_to_cottage.id:
            group_name = f"notes_group_{str(self.request.user.access_to_cottage.id)}"
            async_to_sync(channel_layer.group_send)(
                group_name, # This must match the room name in consumers.py
                {    
                    'type': 'note_message',
                    'data': 'Update notes'
                }
            )
            print("Note websocket message sent to group:", group_name)

        else:
            return Response({'error': 'No cottage active'}, status=status.HTTP_404_NOT_FOUND)

    def perform_destroy(self, instance):
        # 1. Capture the ID before the object is gone from the database
        cottage_id = self.request.user.access_to_cottage.id
        
        # 2. Perform the actual deletion
        instance.delete()
        
        # 3. Trigger the WebSocket
        channel_layer = get_channel_layer()
        if cottage_id:
            group_name = f"notes_group_{str(cottage_id)}"
            async_to_sync(channel_layer.group_send)(
                group_name,
                {    
                    'type': 'note_message',
                    'data': 'Update notes'
                }
            )
            print("Note websocket message sent to group:", group_name)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_note(self, request, pk=None):
        note_instance = self.get_object()
        note_content = request.data.get('note')
        if not note_content:
            return Response({'error': 'Note content is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Use the model's add_note method to add the note
        note_instance.add_note(note_content)
        note_instance.save()

        #Use websockets to notify cottage owners of new task
        channel_layer = get_channel_layer()
        if request.user.access_to_cottage.id:
            group_name = f"notes_group_{str(request.user.access_to_cottage.id)}"
            async_to_sync(channel_layer.group_send)(
                group_name, # This must match the room name in consumers.py
                {    
                    'type': 'note_message',
                    'data': 'Update notes'
                }
            )
            print("Note websocket message sent to group:", group_name)

        return Response({'status': 'note added'}, status=status.HTTP_200_OK)

    @action(
        detail=True, 
        methods=['Delete'], 
        url_path='delete_note/(?P<note_id>[^/.]+)',
        permission_classes=[permissions.IsAuthenticated]
    )
    def delete_note(self, request, pk=None, note_id=None):
        note_instance = self.get_object()
        
        if not note_id:
            return Response({'error': 'Note id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove note from JSON logic
        note_instance.remove_note(note_id)
        note_instance.save() 
        
        #Use websockets to notify cottage owners of new task
        channel_layer = get_channel_layer()
        if request.user.access_to_cottage.id:
            group_name = f"notes_group_{str(request.user.access_to_cottage.id)}"
            async_to_sync(channel_layer.group_send)(
                group_name, # This must match the room name in consumers.py
                {    
                    'type': 'note_message',
                    'data': 'Update notes'
                }
            )
            print("Note websocket message sent to group:", group_name)

        return Response({'status': 'note deleted', 'deleted_id': note_id}, status=status.HTTP_200_OK)