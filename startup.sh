#!/bin/bash
# Startup script for Azure App Service

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Azure App Service provides the PORT environment variable
# Default to 8000 if PORT is not set
PORT=${PORT:-8000}

# Start the FastAPI application with Gunicorn and Uvicorn workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:${PORT} \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
