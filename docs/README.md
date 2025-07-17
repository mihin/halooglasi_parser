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

### 2. Configure Telegram Bot
```bash
# Copy template and add your bot token
cp config.properties.template config.properties

# Edit config.properties - only bot token required:
TELEGRAM_BOT_TOKEN=your_bot_token_here  # Get from @BotFather

# Send a message to your bot → it auto-discovers your chat!
# (Search filters are pre-configured for Belgrade €110k-126k apartments)
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

Automated monitoring (local - 3x daily)
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
2. Add repository secret:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
3. Send a message to your bot from where you want notifications
4. Bot will auto-discover and remember your chat!

### 3. Done!
- ✅ **Runs 3x daily** at 7am, 1pm, 7pm UTC
- ✅ **Zero server costs** (GitHub free tier)
- ✅ **Persistent tracking** - Remembers seen apartments between runs
- ✅ **Auto-discovery** - Bot finds all active chats automatically
- ✅ **Chat persistence** - Chat IDs stored as GitHub Actions artifacts (90-day retention)
- ✅ **Manual trigger**: Actions → HaloOglasi Apartment Parser → Run workflow

### Chat Persistence in GitHub Actions
The bot uses GitHub Actions artifacts to maintain chat state across runs:
- **Storage**: `chat_ids.txt` saved as workflow artifact (excluded from git)
- **Retention**: 90-day automatic renewal keeps chat list persistent
- **Auto-restore**: Each run downloads previous chat state before processing
- **Backup**: Daily workflow maintains artifact freshness
- **Isolation**: Chat data stays private to your repository

## ⚙️ Configuration

### Telegram Setup
The bot automatically discovers and sends notifications to all active chats:

**Option 1: Auto-Discovery (Recommended)**
1. Create bot with @BotFather → get `TELEGRAM_BOT_TOKEN`
2. Send any message to your bot from chats where you want notifications
3. Bot auto-discovers these chats and saves them persistently

**Option 2: Exclusive Single Chat**
```bash
TELEGRAM_CHAT_ID=your_chat_id_here      # EXCLUSIVE mode - disables bot for others
DEBUG_CHAT=your_debug_chat_id_here      # Forces debug messages when no new listings
```

**⚠️ IMPORTANT**: Setting `TELEGRAM_CHAT_ID` enables **EXCLUSIVE MODE**:
- Bot will ONLY send to this specific chat ID
- **Disables the bot for all other users/chats**
- Auto-discovery is completely disabled
- Other users won't receive notifications even if they message the bot

**Chat Management:**
- Auto-discovery: Chats stored in `chat_ids.txt` (GitHub Actions: as artifacts)
- Exclusive mode: Only configured chat receives messages
- Auto-cleanup: Blocked/deleted chats automatically removed
- Multi-chat: Supports private chats, groups, and channels
- Persistent: Chat IDs remembered between runs (local: file, cloud: artifacts)
- Error handling: Continues sending to valid chats if some fail

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
- **📱 Multi-Chat Telegram**: Auto-discovers and sends to all active chats
- **🔍 Debug Mode**: Forces debug messages to specific chat when no new listings found
- **🕐 Automated Scheduling**: Runs 3x daily (7am, 1pm, 7pm) via GitHub Actions
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

## 🔧 Troubleshooting

### Telegram Setup
- **No notifications?** Send a message to your bot first (if auto-discovery mode)
- **Multiple chats?** Bot sends to ALL active chats (auto-discovery mode only)
- **Only want one chat?** Set `TELEGRAM_CHAT_ID` for exclusive mode
- **Group/channel?** Add bot as admin and send a message
- **Chat removed?** Bot auto-removes blocked/deleted chats from `chat_ids.txt`

### Chat Mode Control
```bash
# AUTO-DISCOVERY MODE (default - serves all users)
# TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE  # Leave as default or unset

# EXCLUSIVE MODE (serves only specific chat)
TELEGRAM_CHAT_ID=your_chat_id_here    # Disables bot for other users

# View discovered chats (auto-discovery mode only)
cat chat_ids.txt
```

## 🛠️ Technical Details

### Chat Discovery Process
1. **API Query**: Bot calls Telegram `/getUpdates` to find recent interactions
2. **Multi-Source**: Analyzes messages, edits, channel posts, callback queries
3. **Persistent Storage**: Saves all discovered chat IDs to `chat_ids.txt`
4. **Auto-Cleanup**: Removes chats when bot is blocked/deleted

### Error Handling
- **Graceful Degradation**: If some chats fail, continues to others
- **Auto-Removal**: Problematic chat IDs automatically cleaned up
- **Rate Limiting**: 0.5s delay between messages to avoid Telegram limits
- **Detailed Logging**: Reports success/failure counts per chat

### File Format: `chat_ids.txt`
```
# Telegram Chat IDs - one per line
123456789        # Private chat
-1001234567890   # Group/channel (negative ID)
```
