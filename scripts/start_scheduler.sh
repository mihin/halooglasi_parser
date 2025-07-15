#!/bin/bash

# HaloOglasi Apartment Parser - Scheduler Startup Script
# This script starts the automated apartment monitoring

echo "🏠 HaloOglasi Apartment Parser - Starting Scheduler"
echo "=================================================="

# Change to project root directory
cd "$(dirname "$0")/.."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if requirements are installed
if ! ./venv/bin/python -c "import schedule" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    ./venv/bin/pip install -r requirements.txt
fi

# Check for configuration file
if [ ! -f "config.properties" ]; then
    echo "⚠️  Warning: config.properties not found"
    echo "   Copy config.properties.template to config.properties and update with your credentials"
    echo ""
fi

# Check Telegram configuration
if ! ./venv/bin/python -c "import sys; sys.path.append('src'); from halooglasi_parser.config_loader import config_loader; exit(0 if config_loader.validate_telegram_config() else 1)" 2>/dev/null; then
    echo "⚠️  Warning: Telegram bot not configured"
    echo "   Update TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in config.properties for notifications"
    echo ""
fi

echo "🚀 Starting apartment scheduler..."
echo "📅 Schedule: Every 30 minutes from 8:00 AM to 8:00 PM"
echo "📱 Telegram notifications: $(./venv/bin/python -c "import sys; sys.path.append('src'); from halooglasi_parser.config_loader import config_loader; print('✅ Enabled' if config_loader.validate_telegram_config() else '❌ Not configured')")"
echo "📝 Logs will be saved to: logs/apartment_scheduler.log"
echo ""
echo "🔄 Press Ctrl+C to stop the scheduler"
echo "=================================================="

# Start the scheduler
./venv/bin/python scripts/scheduler.py 