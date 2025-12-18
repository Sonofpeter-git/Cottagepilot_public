from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsReportViewSet, SensorInsightViewSet

router = DefaultRouter()
router.register(r'reports', AnalyticsReportViewSet, basename='analyticsreport')
router.register(r'insights', SensorInsightViewSet, basename='sensorinsight')

urlpatterns = [
    path('', include(router.urls)),
]