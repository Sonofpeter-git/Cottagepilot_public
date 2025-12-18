from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .serializers import NoteSerializer
from .filters import NoteFilter 
from .models import Note

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
        else:
            return Response({'error': 'No cottage active'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_note(self, request, pk=None):
        note_instance = self.get_object()
        note_content = request.data.get('note')
        if not note_content:
            return Response({'error': 'Note content is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Use the model's add_note method to add the note
        note_instance.add_note(note_content)
        note_instance.save()
        return Response({'status': 'note added'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def delete_note(self, request, pk=None):
        note_instance = self.get_object()
        note_id = request.data.get('noteId')
        if not note_id:
            return Response({'error': 'Note id is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        #Remove note from JSON
        note_instance.remove_note(note_id)
        return Response({'status': 'note added'}, status=status.HTTP_200_OK)
