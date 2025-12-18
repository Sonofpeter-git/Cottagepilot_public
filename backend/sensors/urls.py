from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorViewSet, SensorDataViewSet, SensorAlertViewSet

router = DefaultRouter()
router.register(r'sensors', SensorViewSet, basename='sensor')
router.register(r'sensor-data', SensorDataViewSet, basename='sensordata')
router.register(r'alerts', SensorAlertViewSet, basename='sensoralert')

urlpatterns = [
    path('', include(router.urls)),
]
