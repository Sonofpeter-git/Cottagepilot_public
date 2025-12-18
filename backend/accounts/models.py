from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add any additional fields here if needed
    access_to_cottage = models.ForeignKey('cottageInstance.CottageInstanceModel', on_delete=models.CASCADE, related_name='access_to_cottage_accounts', blank=True, null=True)
    user_color = models.CharField(max_length=50, default="#3C86FE")
    pass
