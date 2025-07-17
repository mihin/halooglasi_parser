# Chat ID Management System

This document describes the enhanced Telegram chat ID management system that automatically discovers, stores, and manages multiple chat IDs.

## Features

### 1. Automatic Chat ID Discovery
- Automatically discovers chat IDs by querying the Telegram bot's recent updates
- No manual configuration required when `TELEGRAM_CHAT_ID` is not set
- Supports multiple chat types: private chats, groups, and channels

### 2. Persistent Storage
- Stores all discovered chat IDs in `chat_ids.txt` file in the workspace root
- Persists chat IDs between runs
- Human-readable format with comments
- Automatically creates the file if it doesn't exist

### 3. Exception Handling and Cleanup
- Detects when messages fail due to chat-related errors
- Automatically removes problematic chat IDs (blocked bots, deleted chats, etc.)
- Continues sending to other valid chat IDs even if some fail

### 4. Backward Compatibility
- If `TELEGRAM_CHAT_ID` is configured, uses only that chat ID (no discovery)
- Maintains compatibility with existing configurations
- Graceful fallback behavior

## How It Works

### Configuration Priority

1. **TELEGRAM_CHAT_ID Set**: If `TELEGRAM_CHAT_ID` is configured and not the default value, the system uses only that chat ID
2. **Auto-Discovery**: If `TELEGRAM_CHAT_ID` is not set or is the default, the system:
   - Loads existing chat IDs from `chat_ids.txt`
   - Discovers new chat IDs from bot updates
   - Saves all chat IDs to the file

### Chat ID Discovery Process

1. **API Call**: Makes a GET request to `/getUpdates` endpoint
2. **Parse Updates**: Extracts chat IDs from:
   - Regular messages
   - Edited messages  
   - Channel posts
3. **Store Results**: Saves discovered IDs to the persistent file
4. **Merge**: Combines with existing IDs from previous runs

### Error Handling

The system detects and handles these Telegram API errors:
- `chat not found`
- `forbidden: bot was blocked`
- `forbidden: user is deactivated`
- `forbidden: bot can't initiate conversation`
- `bad request: chat not found`

When these errors occur:
1. The problematic chat ID is automatically removed
2. The `chat_ids.txt` file is updated
3. Sending continues to other valid chat IDs

## File Format: `chat_ids.txt`

```
# Telegram Chat IDs - one per line
# Lines starting with # are comments
123456789
-1001234567890
987654321
```

- One chat ID per line
- Lines starting with `#` are ignored (comments)
- Supports both positive (private chats) and negative (groups/channels) IDs
- Automatically sorted for consistency

## Usage Examples

### Scenario 1: Using Configured Chat ID
```bash
# Set in config.properties or environment
TELEGRAM_CHAT_ID=-1001234567890

# System will use only this chat ID, no discovery
```

### Scenario 2: Auto-Discovery
```bash
# Don't set TELEGRAM_CHAT_ID or set to default
TELEGRAM_CHAT_ID=YOUR_CHAT_ID_HERE

# System will:
# 1. Load existing chat IDs from file
# 2. Discover new chat IDs from bot updates  
# 3. Send to all valid chat IDs
```

### Scenario 3: First Run Setup
1. Create and configure your Telegram bot
2. Send a message to your bot (this creates an update)
3. Run the application - it will automatically discover your chat ID
4. Future runs will use the stored chat ID

## API Functions

### Core Functions

```python
def load_chat_ids() -> set:
    """Load chat IDs from file"""

def save_chat_ids(chat_ids: set):
    """Save chat IDs to file"""

def discover_chat_ids(bot_token: str) -> set:
    """Discover chat IDs from bot updates"""

def remove_chat_id(chat_id: str, chat_ids: set) -> set:
    """Remove problematic chat ID and update file"""

def send_new_apartments_to_telegram(new_apartments, bot_token, configured_chat_id=None):
    """Send apartments to all valid chat IDs"""
```

### Enhanced Message Sending

```python
def send_telegram_message(bot_token: str, chat_id: str, message: str) -> bool | str:
    """
    Send message with enhanced error handling
    Returns:
    - True: Success
    - False: Temporary failure  
    - "REMOVE_CHAT_ID": Permanent failure, chat should be removed
    """
```

## Migration from Old System

The new system is fully backward compatible:

### If you currently use TELEGRAM_CHAT_ID:
- **No changes required**
- System continues to use your configured chat ID
- No auto-discovery occurs

### If you want to use auto-discovery:
- Remove or comment out `TELEGRAM_CHAT_ID` from your config
- Send a message to your bot
- Run the application - it will discover and store your chat ID

## Troubleshooting

### No Chat IDs Discovered
**Symptoms**: "No chat IDs found in recent updates"

**Solution**: 
1. Verify your bot token is correct
2. Send a message to your bot to create an update
3. Run the application again

### Chat ID Removed Automatically
**Symptoms**: "Removed problematic chat ID: XXXXX"

**Causes**:
- User blocked the bot
- Bot was removed from group/channel
- Chat was deleted

**Solution**: Chat IDs are automatically cleaned up, no action needed

### File Permission Issues
**Symptoms**: "Error saving chat IDs to file"

**Solution**: Ensure the application has write permissions to the workspace directory

## Technical Implementation

### File Location
- Path: `{workspace_root}/chat_ids.txt`
- Calculated relative to the main application structure
- Created automatically if missing

### Update Frequency
- Chat IDs are loaded at startup
- New discoveries are immediately saved
- Problematic IDs are removed in real-time
- File is updated on every change

### Rate Limiting
- 0.5 second delay between messages to same chat
- No delay between different chats
- Respects Telegram's rate limits

This system provides robust, automatic chat ID management while maintaining full backward compatibility with existing configurations.