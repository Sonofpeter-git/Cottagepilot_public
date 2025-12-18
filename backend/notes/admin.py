from django.contrib import admin
from .models import Note
# Register your models here.
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'noteClassName', 'notes']
    search_fields = ['noteClassName', 'owner__username']
    readonly_fields = ['id']
