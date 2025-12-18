from django.db import models

class Reservation(models.Model):
    title = models.CharField(max_length=255)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField(blank=True)
    owner = models.ForeignKey('cottageInstance.CottageInstanceModel', on_delete=models.CASCADE, related_name='Reservation_owner', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)
    reservationOwner = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='reservationOwner', blank=True, null=True)

    def __str__(this):
        return this.title