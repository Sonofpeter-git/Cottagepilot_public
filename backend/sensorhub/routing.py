# core/routing.py
from django.urls import re_path
from . import consumers 

# Ensure this is a LIST []
websocket_urlpatterns = [
    re_path(
        r"ws/unified/(?P<cottage_id>\w+)/$", 
        consumers.UnifiedConsumer.as_asgi()
    )
]