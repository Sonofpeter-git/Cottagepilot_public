# gunicorn_config.py

workers = 4  # The number of worker processes
timeout = 90  # Set the worker timeout to 120 seconds

# Bind to a specific host and port
bind = '0.0.0.0:8000'

# Set the maximum number of requests before a worker restarts
max_requests = 200  # Replace 1000 with your desired number

# Optional: Add some jitter to the restarts
max_requests_jitter = 10  # Adds randomness to the number of requests

# Pass the above options to Gunicorn using the `on_reload` hook
def on_reload(server):
    if max_requests is not None:
        max_requests_option = f"--max-requests={max_requests}"
        if max_requests_jitter is not None:
            max_requests_option += f" --max-requests-jitter={max_requests_jitter}"
        server.cmd.append(max_requests_option)