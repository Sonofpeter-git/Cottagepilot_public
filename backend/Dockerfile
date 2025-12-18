# Use official Python image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \
    chromium \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install python dependencies
COPY ./backend/requirements.txt /app/
RUN pip install --upgrade pip
#RUN --mount=type=cache,id=cottagepilot-pip,target=/root/.cache/pip \

RUN pip install -r requirements.txt

# Copy project files
COPY ./backend/ /app/

# Copy supervisord config file
COPY ./backend/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy cron loop script and make it executable
COPY ./backend/run_crons_loop.sh /app/
RUN chmod +x /app/run_crons_loop.sh

# Expose port 8000
EXPOSE 8000

# Start supervisord which runs gunicorn and runcrons
#CMD ["supervisord", "-n"]