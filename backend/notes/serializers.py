from rest_framework import serializers
from .models import Note
from django.contrib.auth import authenticate

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ["id", "noteClassName", "notes"]
