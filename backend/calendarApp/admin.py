from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display =  [
                    'title', 'start', 'end', 'reservationOwner', 'description', 'owner', 'created_at', 'updated_at'
                ]
    list_filter = ['start', 'end', 'owner', 'reservationOwner']
    search_fields = ['start', 'end', 'owner', 'reservationOwner']
    readonly_fields = ['id', 'created_at', 'updated_at']
    ordering = ['-created_at']
