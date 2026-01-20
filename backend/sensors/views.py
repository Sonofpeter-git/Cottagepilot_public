from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt


from .models import Sensor, SensorData, SensorAlert
from .serializers import (
    SensorSerializer, SensorCreateSerializer, SensorClaimSerializer, SensorDataSerializer, SensorDataCreateSerializer,
    SensorAlertSerializer, SensorStatsSerializer)

from .filters import SensorFilter, SensorDataFilter
from django.utils.timezone import now

from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

#Websocket imports
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


#import task model
from tasks.models import Task
import secrets

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SensorViewSet(viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_class = SensorFilter
    search_fields = ['name', 'location', 'type']
    ordering_fields = ['name', 'created_at', 'updated_at', 'status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.access_to_cottage:
            return Sensor.objects.filter(owner=self.request.user.access_to_cottage)
        else:
            return Sensor.objects.none()
    
    def get_permissions(self):
        if self.action == 'create_sensor':
            return [AllowAny()]

        elif self.action == 'add_data':
            sensor = Sensor.objects.filter(sensor_id=self.request.data['sensor_id'], code=self.request.data['code'])
            if sensor:
                return [AllowAny()]
            else:
                return super().get_permissions()
        else:
            return super().get_permissions()
    
    @action(detail=False, methods=['post'])
    def claim_sensor(self, request, *args, **kwargs):
            sensor_id = request.data['sensor_id']
            serializer = SensorCreateSerializer(data=request.data)

            #sensor per plan
            sensorPerPlan = {
                'Basic' : 0,
                'Standard' : 2,
                'Premium': 50   
            }

            if serializer.is_valid():
                try:
                    sensor = Sensor.objects.get(sensor_id = sensor_id)
                    if sensor == None:
                        return Response({'status':'Sensor not found.'}, status=status.HTTP_404_NOT_FOUND)
                    
                    if (sensor.owner == None):
                        print("sensor count:", Sensor.objects.filter(owner=self.request.user.access_to_cottage).count(), "plan limit:", sensorPerPlan[self.request.user.access_to_cottage.stripe_subscription])
                        if (Sensor.objects.filter(owner=self.request.user.access_to_cottage).count()>= sensorPerPlan[self.request.user.access_to_cottage.stripe_subscription]):
                            return Response({'status':'failed', 'message':'Sensor limit reached. Please contact support to upgrade your plan.'}, status=status.HTTP_406_NOT_ACCEPTABLE) 
                        
                        sensor.owner = self.request.user.access_to_cottage
                        sensor.save()

                        response_serializer = SensorSerializer(sensor)

                        return Response({'status':'success',
                                        'results': response_serializer.data}
                                        , status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response({'status':'Sensor already claimed by someone.'}, status=status.HTTP_404_NOT_FOUND)    
                    
                except Exception as e:
                    #Log error to logs
                    print(e)

                    return Response({'status':'An unexpected error occurred.'}, status=status.HTTP_404_NOT_FOUND)
            
            return Response({'status': 'failed',
                            'errors': serializer.errors
                            }, status=status.HTTP_400_BAD_REQUEST)
    

    @action(detail=True, methods=['get'])
    def data(self, request, pk=None):
        """Get sensor data with optional time range filtering"""
        sensor = self.get_object()
        time_range = request.query_params.get('time_range', '24h')
        
        # Calculate time delta based on range
        time_deltas = {
            '1h': timedelta(hours=1),
            '24h': timedelta(hours=24),
            '7d': timedelta(days=7),
            '30d': timedelta(days=30),
        }
        
        start_time = now() - time_deltas[time_range]
        
        data_chunk_size = {
            '1h': 1,    
            '24h': 5,  
            '7d': 45,
            '30d': 90,
        }

        data_points = SensorData.objects.filter(
            sensor=sensor,
            timestamp__gte=start_time
        ).order_by('-timestamp')
        data_points = data_points[::data_chunk_size[time_range]]
        
        serializer = SensorDataSerializer(data_points, many=True)
        return Response({
            'status': 'success',
            'results': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    @csrf_exempt
    def add_data(self, request, pk=None):
        data = request.data
        #prone to cause error if duplicates are created
        sensor = Sensor.objects.get(sensor_id=data['sensor_id'], code=data['code'])
        if not sensor:
            return Response({'status': 'failed', 'errors': 'Sensor not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            sensor_data = SensorData.objects.create(value=data['value'], sensor=sensor)
            sensor_data.full_clean()
            sensor_data.save()
            self.check_limit(sensor, data['value'])
            return Response({'status': 'Success', 'errors':"None"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'status': 'failed', 'errors': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    

    def check_limit(self, sensor, value):
        # Filter Task model for a matching sensor
        tasks = Task.objects.filter(sensor=sensor)
        for task in tasks:
            if float(value) < task.limit_value:
                task.status = 'overdue'
                task.save()


    @action(detail=True, methods=['get'])
    def alerts(self, request, pk=None):
        """Get alerts for a specific sensor"""
        sensor = self.get_object()
        alerts = SensorAlert.objects.filter(sensor=sensor)
        serializer = SensorAlertSerializer(alerts, many=True)
        return Response({
            'status': 'success',
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get sensor statistics for the current user"""
        user_sensors = self.get_queryset()
        
        stats = {
            'total_sensors': user_sensors.count(),
            'active_sensors': user_sensors.filter(status='active').count(),
            'inactive_sensors': user_sensors.filter(status='inactive').count(),
            'error_sensors': user_sensors.filter(status='error').count(),
            'total_data_points': SensorData.objects.filter(sensor__owner=request.user).count(),
            'recent_alerts': SensorAlert.objects.filter(
                sensor__owner=request.user,
                created_at__gte=timezone.now() - timedelta(days=7)
            ).count()
        }
        
        serializer = SensorStatsSerializer(stats)
        return Response({
            'status': 'success',
            'results': serializer.data
        })


class SensorDataViewSet(viewsets.ModelViewSet):
    serializer_class = SensorDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    filterset_class = SensorDataFilter
    ordering_fields = ['timestamp', 'value']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        return SensorData.objects.filter(sensor__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(status='active')

class SensorAlertViewSet(viewsets.ModelViewSet):
    serializer_class = SensorAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    filterset_fields = ['sensor', 'alert_type', 'severity', 'is_resolved']
    ordering_fields = ['created_at', 'severity']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return SensorAlert.objects.filter(sensor__owner=self.request.user)
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Mark an alert as resolved"""
        alert = self.get_object()
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.save()
        
        serializer = self.get_serializer(alert)
        return Response({
            'status': 'success',
            'results': serializer.data
        })
