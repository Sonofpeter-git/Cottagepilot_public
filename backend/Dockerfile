FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (Removed supervisor)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY ./requirements.txt /app/
RUN pip install --upgrade pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Copy project
COPY ./ /app/

# Copy cron loop script and make it executable
COPY run_crons_loop.sh /app/
RUN chmod +x /app/run_crons_loop.sh

EXPOSE 8000

# Default command (can be overridden by docker-compose)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "sensorhub.asgi:application"]