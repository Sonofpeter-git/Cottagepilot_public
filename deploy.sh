#!/bin/bash

# ==========================================
# CONFIGURATION
# ==========================================
REMOTE_USER="niklas"                # CHANGE THIS
REMOTE_HOST="192.168.0.36"      # CHANGE THIS
REMOTE_DIR="/docker/cottagepilot"     # Directory on the server


# Docker Image Names (Must match docker-compose.prod.yml)
BACKEND_IMAGE="sonofpeter1docker/cottagepilot-backend:latest"
NGINX_IMAGE="sonofpeter1docker/cottagepilot-nginx:latest"

# ==========================================
# 1. BUILD LOCALLY
# ==========================================
echo "🚀 Starting Deployment Pipeline..."
echo "📦 Building Docker images locally..."

# Build specific services to ensure we have the latest
docker-compose -f docker-compose.prod.yml build backend nginx

if [ $? -ne 0 ]; then
    echo "❌ Build failed! Aborting."
    exit 1
fi

# ==========================================
# 2. SYNC FILES
# ==========================================
echo "📂 Syncing project files to ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}..."

# Create remote directory if it doesn't exist
ssh ${REMOTE_USER}@${REMOTE_HOST} "mkdir -p ${REMOTE_DIR}"

# Check if rsync is available
if command -v rsync >/dev/null 2>&1; then
    echo "   ... using rsync"
    rsync -avz --delete \
        --exclude '__pycache__' \
        --exclude 'node_modules' \
        --exclude '.git' \
        --exclude '.env' \
        --exclude 'venv' \
        --exclude '.idea' \
        --exclude '.vscode' \
        --exclude '*.sqlite3' \
        ./ ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/
else
    echo "⚠️ rsync not found, falling back to tar + ssh (slower, non-incremental)..."
    # Create excludes file for tar to avoid command line length issues or syntax diffs
    # Note: tar --exclude pattern syntax can vary between BSD/GNU
    # We use a piped tar command to transfer files
    tar --exclude='__pycache__' \
        --exclude='node_modules' \
        --exclude='.git' \
        --exclude='.env' \
        --exclude='venv' \
        --exclude='.idea' \
        --exclude='.vscode' \
        --exclude='*.sqlite3' \
        -czf - . | ssh ${REMOTE_USER}@${REMOTE_HOST} "mkdir -p ${REMOTE_DIR} && tar -xzf - -C ${REMOTE_DIR}"
fi

echo "✅ File sync complete."

# ==========================================
# 3. PUSH IMAGES (SAVE -> SSH -> LOAD)
# ==========================================
echo "🚚 Transferring images to server..."

# Save, compress, and pipe directly to remote docker load
# This avoids using an intermediate registry
echo "   ... Pushing Backend Image (${BACKEND_IMAGE})"
docker save ${BACKEND_IMAGE} | gzip | ssh ${REMOTE_USER}@${REMOTE_HOST} "gunzip | docker load"

echo "   ... Pushing Nginx Image (${NGINX_IMAGE})"
docker save ${NGINX_IMAGE} | gzip | ssh ${REMOTE_USER}@${REMOTE_HOST} "gunzip | docker load"

echo "✅ Images transferred successfully."

# ==========================================
# 4. RESTART SERVICES
# ==========================================
echo "🔄 Restarting remote services..."

ssh ${REMOTE_USER}@${REMOTE_HOST} "cd ${REMOTE_DIR} && docker-compose -f docker-compose.prod.yml up -d --force-recreate"

echo "🎉 Deployment Complete!"
