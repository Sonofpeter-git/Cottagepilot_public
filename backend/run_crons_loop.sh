#!/bin/sh
while true; do
    echo "Running Django cron jobs at $(date)"
    python manage.py runcrons
    sleep 3600  # wait 1h
done