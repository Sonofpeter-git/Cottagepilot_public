#!/bin/bash

# run_crons_loop.sh - Continuously run Django management commands

while true; do
    echo "Running scheduled tasks..."
    python manage.py runcrons
    
    # Wait for 60 seconds before next run (adjust as needed)
    sleep 900
done