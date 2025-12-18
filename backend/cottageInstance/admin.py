from django.contrib import admin
from .models import CottageInstanceModel

# Register your models here.
@admin.register(CottageInstanceModel)
class CottageAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'address', 'id', 'stripe_payment_status']
    list_filter = ['name', 'owner']
    search_fields = ['name', 'address', 'owner']
    readonly_fields = ['id']
    ordering = ['name']
