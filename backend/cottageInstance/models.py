from django.db import models
import uuid

# Create your models here.
class CottageInstanceModel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='CottageMasterModelOwner', blank=True, null=True)
    address = models.CharField(max_length=100)
    
    CottageUsers = models.ManyToManyField(
        'accounts.CustomUser', 
        related_name='cottages', 
        blank=True
    )

    #STRIPE
    stripe_subscription_choices = [
        ('Basic', 'Basic'),
        ('Standard', 'Standard'),
        ('Premium', 'Premium'),
    ]
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_subscription = models.CharField(max_length=15, choices=stripe_subscription_choices, null=True, blank=True)
    stripe_payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    @property
    def stripe_payment_status_int(self):
        return int(self.stripe_payment_status)
    
    @property
    def ownerUsername(self):
        return self.owner.username