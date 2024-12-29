#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Start the FastAPI application with Uvicorn
exec "$@"
