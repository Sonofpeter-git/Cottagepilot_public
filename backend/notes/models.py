
from django.db import models
import uuid
from datetime import timedelta
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.utils import decorators


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('cottageInstance.CottageInstanceModel', on_delete=models.CASCADE, related_name='notes', blank=False, null=False)
    noteClassName = models.CharField(max_length=255)
    #to validate sensor posts
    notes = models.JSONField(default=dict, null=True, blank=True)
    

    def __str__(self):
        return f"{self.noteClassName}"
    
    def add_note(self, value):
        """Add note to class"""     
        unique_id = str(uuid.uuid4())
        self.notes[unique_id] = ({'note' : value, 'time': f'{now()}', 'id': unique_id})
        self.save()


    def remove_note(self, noteId):
        self.notes.pop(noteId)
        self.save()