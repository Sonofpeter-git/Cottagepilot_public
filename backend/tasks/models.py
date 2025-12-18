from django.db import models
import uuid
from datetime import datetime
from sensorhub.settings import AUTH_USER_MODEL
from sensors.models import Sensor
# Create your models here.

class Task(models.Model):
    STATUS_CHOICES = [
      ('done', 'Done'),
      ('in progress', 'In progress'),
      ('waiting', 'Waiting'),
      ('overdue', 'Overdue')
    ]

    MONTH_CHOICES = [
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]
      
    #unique identifier
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #task name
    name = models.CharField(max_length=100)
    #task group
    group = models.CharField(max_length=50, blank=True, null=True)
    
    #task description
    description = models.CharField(max_length=500, blank=True, null=True)
    
    additional_info = models.CharField(max_length=500, blank=True, null=True)
    #task location
    location = models.CharField(max_length=200, null=True, blank=True)
    #task status
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='waiting')
    Responsible_for_the_task = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='Responsible_for_the_task', blank=True, null=True)
    
    #task owner
    owner = models.ForeignKey('cottageInstance.CottageInstanceModel', on_delete=models.CASCADE, related_name='task_owner', blank=True, null=True)
    #automatic fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #task sensor
    sensor=models.ForeignKey(Sensor, on_delete=models.CASCADE, null=True, blank=True)
    #limit_value when notification is sent
    limit_value = models.IntegerField(null=True, blank=True)
    #is the task for a month
    month_correlation = models.CharField(choices=MONTH_CHOICES, max_length=20, blank=True, null=True)
    
    #time to the next alert
    time_correlation = models.DateField(blank=True, null=True)
    #linked to Reservation
    linked_to_reservation = models.ForeignKey('calendarApp.Reservation', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.location})"

    def update_status(self):
        self.status=("overdue")
        self.save()
        return 

    def get_tasks_in_group(self, group_name):
        tasks_in_group = Task.objects.filter(group=group_name)
        return tasks_in_group