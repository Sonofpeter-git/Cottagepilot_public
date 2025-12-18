from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Max, Min, Count
from django.utils import timezone
from datetime import timedelta

from .models import AnalyticsReport, SensorInsight
from .serializers import AnalyticsReportSerializer, SensorInsightSerializer
from sensors.models import Sensor, SensorData


class AnalyticsReportViewSet(viewsets.ModelViewSet):
    serializer_class = AnalyticsReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return AnalyticsReport.objects.filter(sensors__owner=self.request.user).distinct()


class SensorInsightViewSet(viewsets.ModelViewSet):
    serializer_class = SensorInsightSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return SensorInsight.objects.filter(sensor__owner=self.request.user)
    
    @action(detail=False, methods=['get'])
    def generate_insights(self, request):
        """Generate insights for user's sensors"""
        user_sensors = Sensor.objects.filter(owner=request.user)
        insights = []
        
        for sensor in user_sensors:
            # Generate trend analysis
            recent_data = SensorData.objects.filter(
                sensor=sensor,
                timestamp__gte=timezone.now() - timedelta(days=7)
            ).aggregate(
                avg_value=Avg('value'),
                max_value=Max('value'),
                min_value=Min('value'),
                count=Count('id')
            )
            
            if recent_data['count'] > 0:
                insight_data = {
                    'average': recent_data['avg_value'],
                    'maximum': recent_data['max_value'],
                    'minimum': recent_data['min_value'],
                    'data_points': recent_data['count']
                }
                
                # Create or update insight
                insight, created = SensorInsight.objects.get_or_create(
                    sensor=sensor,
                    insight_type='trend',
                    defaults={
                        'title': f'7-Day Trend Analysis for {sensor.name}',
                        'description': f'Average reading: {recent_data["avg_value"]:.2f} {sensor.unit}',
                        'confidence_score': 0.85,
                        'data': insight_data
                    }
                )
                
                if not created:
                    insight.data = insight_data
                    insight.description = f'Average reading: {recent_data["avg_value"]:.2f} {sensor.unit}'
                    insight.save()
                
                insights.append(insight)
        
        serializer = self.get_serializer(insights, many=True)
        return Response({
            'status': 'success',
            'data': serializer.data
        })