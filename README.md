# HaloOglasi Apartment Parser

🏠 **Automated apartment monitoring for Belgrade, Serbia** - Finds new listings on HaloOglasi.com and sends instant Telegram notifications.

## 🚀 Quick Start (Local)

**Requirements**: Python 3.11+ (required for numpy 2.2+ compatibility)

### 1. Setup
```bash
git clone https://github.com/shestakovitch/halooglasi_parser.git
cd halooglasi_parser
pip install -r requirements.txt
```

### 2. Configure Settings (Optional)
```bash
# Copy the template and customize settings
cp config.properties.template config.properties

# Edit config.properties for:
TELEGRAM_BOT_TOKEN=your_bot_token_here  # Get from @BotFather
TELEGRAM_CHAT_ID=your_chat_id_here      # Get from @userinfobot

# Search filters (optional - defaults provided):
SEARCH_TYPE=buy                         # 'buy' or 'rent'
PRICE_FROM=110000                       # Min price in euros
PRICE_TO=126000                         # Max price in euros
APARTMENT_AREA_FROM=45                  # Min area in m²
NUMBER_OF_ROOMS_FROM=4                  # Min rooms (system value)
NUMBER_OF_ROOMS_TO=9                    # Max rooms (system value)
```

### 3. Run
```bash
cd scripts
python run_search.py
```
or 
```bash
make run
```

Automated monitoring (local)
```bash
cd scripts && python scheduler.py
```
or 
```bash
make schedule
```

## ☁️ GitHub Actions (Recommended)

**Free automated cloud deployment - no server needed!**

### 1. Setup Repository
1. **Fork this repository** to your GitHub account
2. **Enable Actions**: Go to Actions tab → Enable workflows

### 2. Configure Secrets
1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add repository secrets:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
   - `TELEGRAM_CHAT_ID`: Your Telegram chat ID

### 3. Done!
- ✅ **Runs every 30 minutes** from 8am-8pm UTC daily
- ✅ **Zero server costs** (GitHub free tier)
- ✅ **Persistent tracking** - Remembers seen apartments between runs
- ✅ **Manual trigger**: Actions → HaloOglasi Apartment Parser → Run workflow

## ⚙️ Configuration

### Search Settings (config.properties or environment variables)
```bash
SEARCH_TYPE=buy            # 'buy' or 'rent'
PRICE_FROM=110000          # Min price (€)
PRICE_TO=126000            # Max price (€)
APARTMENT_AREA_FROM=45     # Min area (m²)
NUMBER_OF_ROOMS_FROM=4     # Min rooms (=2.0 rooms)
NUMBER_OF_ROOMS_TO=9       # Max rooms (=4.5 rooms)
FLOOR_FROM=PR              # Floor preference (PR=ground floor)
```

### App Settings (scripts/run_search.py)
```python
EXPORT_TO_TELEGRAM = True  # Send to Telegram bot
EXPORT_TO_EXCEL = False    # Generate Excel file (slower)
MAX_DAYS_OLD = 2           # Output apartments from last 2 days (console/excel)
```

## 🆕 Key Features

- **🎯 Smart Tracking**: Only shows NEW apartments (never seen before)
- **📱 Telegram Notifications**: Instant alerts for new listings
- **🕐 Automated Scheduling**: Runs every 30min during business hours (GitHub Actions)
- **💾 ID Persistence**: Tracks seen apartments locally or in cloud
- **📊 Rich Data**: Price/m², location, rooms, agent type, photos
- **⚡ Fast Mode**: Excel export disabled by default

## 📱 Sample Output

**Console:**
```
🆕 NEW APARTMENTS (3 total)
📅 15.07.2025. (3 new listings)

1. 📝 Beautiful apartment in center
   💰 €121.500 • 2.209 €/m² 🆕
   🏘️ Rakovica
   🔗 https://www.halooglasi.com/...
   🏠 55 m² • 2.5 rooms
   👤 Agency • 14 images
```

**Telegram:**
```
📝 Beautiful apartment in center
💰 €121.500 • 2.209 €/m² 🆕
🏘️ Rakovica
🔗 View on HaloOglasi
🏠 55 m² • 2.5 rooms
👤 Agency • 14 images
```
## 📋 Current Search Criteria

- **Type**: Apartments for purchase (not rent)
- **Location**: Belgrade (51 specific areas, excludes remote suburbs)
- **Price**: €110,000 - €126,000
- **Area**: 45m² minimum
- **Rooms**: 2.0 - 4.5 rooms
- **Legal**: Legally registered only
