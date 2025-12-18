import django_filters
from django.utils import timezone
from datetime import timedelta
from .models import Note


class NoteFilter(django_filters.FilterSet):
    id = django_filters.CharFilter()
    noteClassName = django_filters.CharFilter()
    notes = django_filters.CharFilter()

    class Meta:
        model = Note
        fields = ["id", "noteClassName", "notes"]
