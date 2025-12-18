from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sensorhub.settings')

from backend.celery_app import app as celery_app

__all__ = ('celery_app',)
