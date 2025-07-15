# HaloOglasi Apartment Parser

🏠 **Automated apartment monitoring for Belgrade, Serbia** - Finds new listings on HaloOglasi.com and sends instant Telegram notifications.

## 🚀 Quick Start

**Requirements**: Python 3.11+ (required for numpy 2.2+ compatibility)

### 1. Setup
```bash
git clone https://github.com/shestakovitch/halooglasi_parser.git
cd halooglasi_parser

# Quick setup with Makefile
make setup

# Or manual setup:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Credentials (Optional)

**Option A: Properties File (Recommended for local development)**
```bash
# Copy the template and add your credentials
cp config.properties.template config.properties

# Edit config.properties and replace:
TELEGRAM_BOT_TOKEN=your_bot_token_here  # Get from @BotFather
TELEGRAM_CHAT_ID=your_chat_id_here      # Get from @userinfobot
```

**Option B: Environment Variables (Recommended for production/containers)**
```bash
# Set environment variables (highest priority)
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"

# Test configuration
make test-env
```

### 3. Run Options

**Single Search:**
```bash
make run
# or: python scripts/run_search.py
```

**Automated Monitoring (Recommended):**
```bash
make schedule
# or: ./scripts/start_scheduler.sh
```

## 🌐 Deployment to Python Server

### Quick Deploy (VPS/Cloud)
```bash
# 1. Upload to server
scp -r halooglasi_parser user@server:/home/user/

# 2. Setup on server
ssh user@server
cd halooglasi_parser
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure credentials  
cp config.properties.template config.properties
nano config.properties

# 4. Start monitoring
./start_scheduler.sh
```

### Production Deployment (systemd)
```bash
# Create service file
sudo nano /etc/systemd/system/halooglasi.service

# Add content (with environment variables):
[Unit]
Description=HaloOglasi Apartment Parser
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/halooglasi_parser
Environment=TELEGRAM_BOT_TOKEN=your_actual_token_here
Environment=TELEGRAM_CHAT_ID=your_actual_chat_id_here
ExecStart=/path/to/halooglasi_parser/venv/bin/python scripts/scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable halooglasi
sudo systemctl start halooglasi
sudo systemctl status halooglasi
```

### Background Deployment (screen/tmux)
```bash
# Using screen
screen -dmS halooglasi ./start_scheduler.sh
screen -r halooglasi  # to reattach

# Using tmux
tmux new-session -d -s halooglasi './start_scheduler.sh'
tmux attach-session -t halooglasi  # to reattach
```

## ⚙️ Configuration

### Basic Settings (main.py)
```python
MAX_DAYS_OLD = 2           # Show apartments from last 2 days
EXPORT_TO_EXCEL = False    # Generate Excel file (slower)
EXPORT_TO_TELEGRAM = True  # Send to Telegram bot
```

### Search Criteria (config.py)
```python
price_from = '110000'      # Min price (€)
price_to = '126000'        # Max price (€)
apartment_area_from = 45   # Min area (m²)
number_of_rooms_from = '4' # Min rooms (system value)
number_of_rooms_to = '9'   # Max rooms (system value)
```

## 🆕 Key Features

- **🎯 Smart Tracking**: Only shows NEW apartments (never seen before)
- **📱 Telegram Notifications**: Instant alerts for new listings
- **🕐 Automated Scheduling**: Runs every 30min during business hours
- **💾 ID Persistence**: Tracks seen apartments locally
- **📊 Rich Data**: Price/m², location, rooms, agent type, photos
- **⚡ Fast Mode**: Excel export disabled by default
- **📋 Comprehensive Logs**: Full activity logging

## 📱 Sample Output

**Console:**
```
🆕 NEW APARTMENTS (3 total)
📅 15.07.2025. (3 new listings)

1. 💰 €121.500 🆕
   📍 Rakovica
   📐 55m² • 2.5 rooms • 2.209 €/m²
   👤 Agency • 14 images
   🔗 https://www.halooglasi.com/...
```

**Telegram Message:**
```
🆕 NEW APARTMENT FOUND!

💰 €121.500
📍 Location: Rakovica
📐 Details: 55m² • 2.5 rooms • 2.209 €/m²
👤 Agent: Agency
📷 Photos: 14 images
📅 Published: 15.07.2025.

🔗 View on HaloOglasi
```

## 🔧 Commands

```bash
# Manual search
python3 main.py

# Start automated monitoring
./start_scheduler.sh
python3 scheduler.py

# View logs
tail -f apartment_scheduler.log

# Stop scheduler
# Press Ctrl+C in scheduler terminal
```

## ☁️ GitHub Actions Deployment (Recommended)

The easiest way to run this automatically in the cloud using GitHub's free tier:

### 1. Setup Repository
1. **Fork this repository** to your GitHub account
2. **Enable Actions**: Go to Actions tab → Enable workflows

### 2. Configure Secrets
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add repository secrets:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
   - `TELEGRAM_CHAT_ID`: Your Telegram chat ID

### 3. Automatic Execution
- ✅ **Runs every 30 minutes** from 8am-8pm UTC daily
- ✅ **Zero server costs** (GitHub free tier)
- ✅ **No maintenance** required
- ✅ **Built-in logging** and artifact storage
- ✅ **Persistent tracking** - Remembers seen apartments between runs

### 4. Monitoring
- **View runs**: Actions tab → HaloOglasi Apartment Parser
- **Manual trigger**: Run workflow button
- **Download logs**: Artifacts section in each run
- **Check status**: Green ✅ = success, Red ❌ = failed

### 5. Benefits
- 🆓 **Free hosting** on GitHub infrastructure
- 🔄 **Automatic updates** when you push changes
- 📊 **Built-in monitoring** and alerting
- 🚀 **One-time setup**, runs forever
- 🧹 **Clean storage** - No file accumulation between runs

## 📋 Current Search Criteria

- **Type**: Apartments for purchase (not rent)
- **Location**: Belgrade (51 specific areas, excludes remote suburbs)
- **Price**: €110,000 - €126,000
- **Area**: 45m² minimum
- **Rooms**: 2.0 - 4.5 rooms
- **Floor**: Ground floor minimum
- **Legal**: Legally registered only
- **Condition**: Excludes renovation needed

## 📁 Output Files

- `apartment_scheduler.log` - Scheduler activity log
- `previous_apartment_ids.json` - Tracked apartment IDs
- `halooglasi_data.json` - Raw API response
- `halooglasi_data.xlsx` - Excel export (if enabled)

## 🛠️ Development

### Switching Buy ↔ Rent
```python
# In config.py for rental search:
'CategoryId': '13'           # 13=rent, 1=buy
'SearchTypeIds': [2, 3]      # Rental types
'BaseTaxonomy': '/nekretnine/izdavanje-stanova'
```

### Custom Locations
Modify `FieldValues` array in `config.py` with Belgrade area IDs.

### Schedule Modification
Change timing in `scheduler.py`:
```python
start_time = dt_time(8, 0)   # 8:00 AM
end_time = dt_time(20, 0)    # 8:00 PM
schedule.every(30).minutes   # Every 30 minutes
```

## 📊 Architecture

- **main.py** - Core search logic
- **scheduler.py** - Automated scheduling
- **parser.py** - HTML parsing & data extraction
- **scraper.py** - API requests
- **exporter.py** - Console output & Excel
- **telegram_exporter.py** - Telegram notifications
- **id_manager.py** - Apartment ID tracking
- **config.py** - Search parameters & credentials

Perfect for real estate monitoring, property investment research, and apartment hunting automation!
