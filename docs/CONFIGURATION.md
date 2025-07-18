# Configuration Guide

## Overview

The HaloOglasi Parser uses a secure configuration system that separates sensitive credentials from the codebase. This follows security best practices by keeping secrets in gitignored files.

## Configuration Files

### 1. `config.properties` (Gitignored - Contains Secrets)
This file contains your actual credentials and sensitive configuration. It's automatically ignored by git for security.

```properties
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
TELEGRAM_CHAT_ID=your_actual_chat_id_here
```

### 2. `config.properties.template` (Committed - Safe Template)
This is the template file that's safely committed to version control. Copy this file to create your `config.properties`.

### 3. `src/halooglasi_parser/config.py` (Main Configuration)
Contains non-sensitive configuration like search parameters, API endpoints, and loads credentials from the properties file.

## Setup Instructions

### 1. Create Configuration File
```bash
# Copy the template
cp config.properties.template config.properties
```

### 2. Update Credentials
Edit `config.properties` with your actual values:

```properties
# Get from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNOPqrsTUVwxyz

# Get from @userinfobot on Telegram  
TELEGRAM_CHAT_ID=-1001234567890

# Optional: Forces debug messages when no new listings found
DEBUG_CHAT=-1001234567891
```

### 3. Verify Configuration
```bash
# Test the configuration
python -c "
import sys; sys.path.append('src')
from halooglasi_parser.config_loader import config_loader
print('Telegram configured:', config_loader.validate_telegram_config())
"
```

## Configuration Priority

The system loads configuration in this priority order:

1. **Environment Variables** (highest priority)
2. **Properties File** (`config.properties`)
3. **Default Values** (lowest priority)

### Using Environment Variables
You can override any setting using environment variables:

```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
python scripts/run_search.py
```

## Security Features

### ✅ What's Protected
- `config.properties` - Gitignored, contains actual secrets
- `data/` directory - Contains apartment data and IDs
- `logs/` directory - Contains operational logs

### ✅ What's Safe to Commit
- `config.properties.template` - Template with placeholders
- `src/halooglasi_parser/config.py` - Uses loader, no hardcoded secrets
- All other source code files

## Configuration Options

### Current Configuration Options

#### Secrets (Sensitive Data)
- `TELEGRAM_BOT_TOKEN` - Bot token from @BotFather (Required)
- `TELEGRAM_CHAT_ID` - Optional: Specific chat ID for **EXCLUSIVE MODE** (disables bot for other users)

#### Variables (Non-Sensitive Configuration)
- `DEBUG_CHAT` - Optional debug chat ID that forces sending most recent listing when no new listings found
- `SEARCH_TYPE` - 'buy' or 'rent' (default: buy)
- `PRICE_FROM` - Minimum price in euros (default: 110000)
- `PRICE_TO` - Maximum price in euros (default: 126000)
- `APARTMENT_AREA_FROM` - Minimum area in m² (default: 45)
- `APARTMENT_AREA_TO` - Maximum area in m²
- `NUMBER_OF_ROOMS_FROM` - Minimum rooms (default: 4 = 2.0 rooms)
- `NUMBER_OF_ROOMS_TO` - Maximum rooms (default: 9 = 4.5 rooms)
- `FLOOR_FROM` - Minimum floor (default: PR = ground floor)
- `FLOOR_TO` - Maximum floor
- `NOTIFICATION_INTERVAL_HOURS` - Hours between notifications (default: 6)

> **⚠️ IMPORTANT**: Setting `TELEGRAM_CHAT_ID` enables **EXCLUSIVE MODE** - the bot will ONLY serve that specific chat and will be disabled for all other users.

> **💡 Tip**: For multi-user bot setup, leave `TELEGRAM_CHAT_ID` unset to enable auto-discovery mode.

### Future Extensibility
The system is designed to easily add new credentials:

```properties
# API Configuration
API_KEY=your_api_key_here
API_SECRET=your_api_secret_here

# Database Configuration  
DB_PASSWORD=your_db_password_here
DB_HOST=localhost
DB_USER=your_db_user_here

# Email Configuration
EMAIL_PASSWORD=your_email_password_here
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

## Troubleshooting

### Configuration Not Found
If you see: `Warning: config.properties not found`
```bash
cp config.properties.template config.properties
# Edit the file with your credentials
```

### Telegram Not Configured
If you see: `Warning: Telegram bot not configured`
1. Check your `config.properties` file exists
2. Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are set
3. Make sure values don't contain placeholder text

### Environment Override
To temporarily override configuration:
```bash
TELEGRAM_BOT_TOKEN="temp_token" python scripts/run_search.py
```

## GitHub Actions Configuration

For GitHub Actions deployment, configuration is handled through GitHub's Secrets and Variables:

### Setup Instructions
1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
2. Click the **Secrets** tab and add:
   - `TELEGRAM_BOT_TOKEN`: Your bot token from @BotFather
   - `TELEGRAM_CHAT_ID`: (Optional) For exclusive mode
3. Click the **Variables** tab and add any of:
   - `DEBUG_CHAT`: Debug chat ID
   - `SEARCH_TYPE`: Search type (buy/rent)
   - `PRICE_FROM`: Minimum price
   - `PRICE_TO`: Maximum price
   - `APARTMENT_AREA_FROM`: Minimum area
   - `APARTMENT_AREA_TO`: Maximum area
   - `NUMBER_OF_ROOMS_FROM`: Minimum rooms
   - `NUMBER_OF_ROOMS_TO`: Maximum rooms
   - `FLOOR_FROM`: Minimum floor
   - `FLOOR_TO`: Maximum floor

### Configuration Priority
GitHub Actions uses this order:
1. **Repository Variables** (for non-sensitive config)
2. **Repository Secrets** (for sensitive data like tokens)
3. **Default Values** (built into the code)

## Best Practices

1. **Never commit secrets** - Always use `config.properties` for sensitive data
2. **Use environment variables** - For containerized deployments
3. **Use GitHub Variables** - For non-sensitive configuration in cloud deployments
4. **Keep template updated** - When adding new configuration options
5. **Validate configuration** - Test with `config_loader.validate_telegram_config()`
6. **Document new options** - Update this guide when adding new credentials 