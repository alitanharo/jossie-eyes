#!/bin/bash
# Jossie Eyes - Raspberry Pi Startup Script
# Run this on boot to start the Jossie Eyes application

set -e

echo "========================================="
echo "  Jossie Eyes - Starting..."
echo "========================================="
echo ""

# Project directory (adjust as needed)
PROJECT_DIR="/home/pi/jossie-eyes"
LOG_FILE="$PROJECT_DIR/jossie-eyes.log"

# Change to project directory
cd "$PROJECT_DIR"

# Check internet connectivity
echo "Checking internet connectivity..."
if ! ping -c 1 8.8.8.8 &> /dev/null; then
    echo "WARNING: No internet connection detected"
    # Play offline warning sound
    if command -v espeak &> /dev/null; then
        espeak "Warning: No internet connection. Some features may be limited."
    fi
fi

# Check if environment file exists
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please run the deployment script first."
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating Python virtual environment..."
    source venv/bin/activate
fi

# Start the edge device
echo "Starting Jossie Eyes edge device..."
echo "$(date): Starting Jossie Eyes" >> "$LOG_FILE"

python src/edge_device.py 2>&1 | tee -a "$LOG_FILE"

echo ""
echo "Jossie Eyes stopped."