from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import healtCheck, makePwd


urlpatterns = [
    path('backend/admin/', admin.site.urls),
    path('', include('sensors.urls')),
    path('', include('tasks.urls')),
    path('', include('accounts.urls')),
    path('', include('notes.urls')),
    path('', include('calendarApp.urls')),
    path('', include('stripeApp.urls')),
    path('cottage/', include('cottageInstance.urls')),
    path('analytics/', include('analytics.urls')),
    path('health/', healtCheck, name="healtCheck"),
    path('', healtCheck, name="healtCheck"),
    path('makePWD/', makePwd, name="makePwd"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
