import requests
import json
import os
from datetime import datetime


def get_chat_ids_file_path():
    """Get the path to the chat IDs file in data/ directory"""
    # Try multiple potential locations for chat_ids.txt in data/ directory
    
    # Option 1: data/ directory relative to workspace root
    workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_workspace_path = os.path.join(workspace_root, 'data', 'chat_ids.txt')
    
    # Option 2: data/ directory relative to current working directory
    data_cwd_path = os.path.join(os.getcwd(), 'data', 'chat_ids.txt')
    
    # Option 3: data/ directory relative to scripts parent (if running from scripts/)
    data_scripts_parent_path = os.path.join(os.path.dirname(os.getcwd()), 'data', 'chat_ids.txt')
    
    print(f"🔍 Checking chat_ids.txt locations in data/ directory:")
    print(f"  1. Workspace data/: {data_workspace_path} (exists: {os.path.exists(data_workspace_path)})")
    print(f"  2. Current data/: {data_cwd_path} (exists: {os.path.exists(data_cwd_path)})")
    print(f"  3. Parent data/: {data_scripts_parent_path} (exists: {os.path.exists(data_scripts_parent_path)})")
    
    # Return the first existing file, prioritizing current working directory over parent
    if os.path.exists(data_cwd_path):
        print(f"✅ Using current data/ path: {data_cwd_path}")
        return data_cwd_path
    elif os.path.exists(data_workspace_path):
        print(f"✅ Using workspace data/ path: {data_workspace_path}")
        return data_workspace_path
    elif os.path.exists(data_scripts_parent_path):
        print(f"✅ Using parent data/ path: {data_scripts_parent_path}")
        return data_scripts_parent_path
    else:
        print(f"📂 No existing file found, will use current data/: {data_cwd_path}")
        return data_cwd_path


def load_chat_ids():
    """Load chat IDs from file"""
    chat_ids_file = get_chat_ids_file_path()
    chat_ids = set()
    
    if os.path.exists(chat_ids_file):
        try:
            with open(chat_ids_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        chat_ids.add(line)
            print(f"📂 Loaded {len(chat_ids)} chat IDs from {chat_ids_file}")
        except Exception as e:
            print(f"❌ Error loading chat IDs from file: {e}")
    else:
        print(f"📂 Chat IDs file not found, will create: {chat_ids_file}")
    
    return chat_ids


def save_chat_ids(chat_ids):
    """Save chat IDs to file"""
    chat_ids_file = get_chat_ids_file_path()
    
    try:
        with open(chat_ids_file, 'w') as f:
            f.write("# Telegram Chat IDs - one per line\n")
            f.write("# Lines starting with # are comments\n")
            for chat_id in sorted(chat_ids):
                f.write(f"{chat_id}\n")
        print(f"💾 Saved {len(chat_ids)} chat IDs to {chat_ids_file}")
    except Exception as e:
        print(f"❌ Error saving chat IDs to file: {e}")


def get_telegram_updates(bot_token, limit=100):
    """Get recent updates from Telegram to find all active chat IDs"""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    params = {
        "limit": limit,
        "timeout": 10
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get Telegram updates: {e}")
        return None


def discover_chat_ids(bot_token):
    """Discover chat IDs by getting updates from Telegram bot"""
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('ok'):
            print(f"❌ Telegram API error: {data.get('description', 'Unknown error')}")
            return set()
        
        chat_ids = set()
        updates = data.get('result', [])
        
        for update in updates:
            # Check for message
            if 'message' in update:
                chat_id = update['message']['chat']['id']
                chat_ids.add(str(chat_id))
            
            # Check for edited message
            if 'edited_message' in update:
                chat_id = update['edited_message']['chat']['id']
                chat_ids.add(str(chat_id))
            
            # Check for channel post
            if 'channel_post' in update:
                chat_id = update['channel_post']['chat']['id']
                chat_ids.add(str(chat_id))
        
        if chat_ids:
            print(f"🔍 Discovered {len(chat_ids)} chat IDs from Telegram updates")
            for chat_id in chat_ids:
                print(f"  📋 Chat ID: {chat_id}")
        else:
            print("🔍 No chat IDs found in recent updates. Send a message to your bot to discover chat IDs.")
        
        return chat_ids
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to discover chat IDs: {e}")
        return set()


def get_active_chat_ids(bot_token):
    """Get all active chat IDs from recent updates"""
    updates_data = get_telegram_updates(bot_token)
    
    if not updates_data or not updates_data.get('ok'):
        print("❌ Failed to retrieve Telegram updates")
        return []
    
    chat_ids = set()
    updates = updates_data.get('result', [])
    
    for update in updates:
        # Check for different types of messages
        message = None
        if 'message' in update:
            message = update['message']
        elif 'edited_message' in update:
            message = update['edited_message']
        elif 'channel_post' in update:
            message = update['channel_post']
        elif 'edited_channel_post' in update:
            message = update['edited_channel_post']
        elif 'callback_query' in update and 'message' in update['callback_query']:
            message = update['callback_query']['message']
        
        if message and 'chat' in message:
            chat_id = message['chat']['id']
            chat_ids.add(str(chat_id))
    
    # Convert to list and filter out empty results
    active_chat_ids = list(chat_ids)
    
    if active_chat_ids:
        print(f"📋 Found {len(active_chat_ids)} active chat(s): {active_chat_ids}")
    else:
        print("⚠️ No active chats found in recent updates")
    
    return active_chat_ids


def remove_chat_id(chat_id, chat_ids):
    """Remove a chat ID from the set and save to file"""
    if chat_id in chat_ids:
        chat_ids.remove(chat_id)
        save_chat_ids(chat_ids)
        print(f"🗑️ Removed problematic chat ID: {chat_id}")
    return chat_ids


def send_telegram_message(bot_token, chat_id, message, parse_mode="HTML"):
    """Send a message to Telegram bot"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": False
    }
    
    response = None
    try:
        response = requests.post(url, data=data, timeout=30)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send Telegram message to chat {chat_id}: {e}")
        
        # Check if it's a chat-related error (chat not found, bot blocked, etc.)
        if response is not None:
            try:
                error_data = response.json()
                error_description = error_data.get('description', '').lower()
                
                # Common errors that indicate the chat ID should be removed
                chat_errors = [
                    'chat not found',
                    'forbidden: bot was blocked',
                    'forbidden: user is deactivated',
                    'forbidden: bot can\'t initiate conversation',
                    'bad request: chat not found'
                ]
                
                if any(error in error_description for error in chat_errors):
                    print(f"🚫 Chat error detected for {chat_id}: {error_description}")
                    return "REMOVE_CHAT_ID"
                    
            except:
                pass
        
        return False


def format_apartment_for_telegram(apartment, is_debug=False):
    """Format apartment data for Telegram message - matches console output order"""
    price = format_price(apartment['price'])
    
    # Match console output order exactly:
    # 1. Title, Price, Price/m²
    # 2. Location  
    # 3. Link
    # 4. All other details (features)
    # 5. Description
    # 6. Agent info at the end
    
    message_parts = []
    
    # Add DEBUG marker if this is a debug message
    if is_debug:
        message_parts.append("🔍 <b>DEBUG</b> - Most recent listing (no new apartments found)")
        message_parts.append("")  # Empty line for separation
    
    # 1. Title, Price, Price/m² 
    message_parts.append(f"📝 <b>{apartment['title']}</b>")
    debug_marker = "" if is_debug else " 🆕"
    message_parts.append(f"💰 <b>{price} • {apartment['price_per_m2']}</b>{debug_marker}")
    
    # 2. Location
    if apartment['subtitle_places'] != "N/A":
        message_parts.append(f"🏘️ {apartment['subtitle_places']}")
    
    # 3. Link
    message_parts.append(f"🔗 <a href=\"{apartment['link']}\">View on HaloOglasi</a>")
    
    # 4. All other details (features)
    if apartment['product_features'] != "N/A":
        # Remove "Kvadratura" from product features - same as console
        features_clean = apartment['product_features'].replace('Kvadratura', '').replace('  ', ' ').strip()
        message_parts.append(f"🏠 {features_clean}")
    
    # 5. Description
    if apartment['description'] != "N/A":
        # Truncate long descriptions for Telegram
        description = apartment['description']
        if len(description) > 200:
            description = description[:200] + "..."
        message_parts.append(f"📋 {description}")
    
    # 6. Agent info at the end
    message_parts.append(f"👤 {apartment['agent_type']} • {apartment['image_count']}")
    
    if is_debug:
        message_parts.append("")  # Empty line for separation
        message_parts.append("ℹ️ This is a debug message showing the most recent apartment found.")
    
    return "\n".join(message_parts)


def format_price(price):
    """Format price with thousands separator"""
    if price == "N/A":
        return "N/A"
    return f"€{price:,}".replace(",", ".")


def send_new_apartments_to_telegram(new_apartments, bot_token, configured_chat_id=None):
    """Send each new apartment as a separate Telegram message to all chat IDs"""
    if not new_apartments:
        print("📱 No new apartments to send to Telegram")
        return
    
    if bot_token == "YOUR_BOT_TOKEN_HERE":
        print("❌ Please configure TELEGRAM_BOT_TOKEN in config.py")
        return
    
    # Determine which chat IDs to use
    chat_ids = set()
    
    # Check if DEBUG_CHAT is configured - if so, disable auto-discovery and only use DEBUG_CHAT
    from .config import DEBUG_CHAT
    debug_configured = (DEBUG_CHAT and 
                       DEBUG_CHAT.strip() != "" and 
                       DEBUG_CHAT not in ["YOUR_DEBUG_CHAT_ID_HERE", "YOUR_CHAT_ID_HERE", "YOUR_TELEGRAM_CHAT_ID_HERE"] and
                       not DEBUG_CHAT.startswith("YOUR_") and
                       not DEBUG_CHAT.endswith("_HERE"))
    
    # If TELEGRAM_CHAT_ID is explicitly configured, use ONLY that one (disable auto-discovery)
    if (configured_chat_id and 
        configured_chat_id not in ["YOUR_CHAT_ID_HERE", "YOUR_TELEGRAM_CHAT_ID_HERE", "", None] and
        not configured_chat_id.startswith("YOUR_") and
        not configured_chat_id.endswith("_HERE")):
        chat_ids.add(configured_chat_id)
        print(f"📱 EXCLUSIVE MODE: Using only configured TELEGRAM_CHAT_ID: {configured_chat_id}")
        print(f"📱 Auto-discovery disabled - bot will ONLY send to this chat")
    elif debug_configured:
        # If DEBUG_CHAT is configured, disable auto-discovery and use only loaded chat IDs
        print(f"📱 DEBUG MODE: DEBUG_CHAT configured, skipping auto-discovery")
        chat_ids = load_chat_ids()
    else:
        # Auto-discovery mode: Load existing chat IDs from file and discover new ones
        print(f"📱 AUTO-DISCOVERY MODE: TELEGRAM_CHAT_ID not set, discovering active chats")
        chat_ids = load_chat_ids()
        
        # Discover new chat IDs using both methods
        discovered_ids = discover_chat_ids(bot_token)
        active_ids = set(str(chat_id) for chat_id in get_active_chat_ids(bot_token))
        
        # Combine discovered IDs from both methods
        all_discovered = discovered_ids.union(active_ids)
        
        if all_discovered:
            original_count = len(chat_ids)
            chat_ids.update(all_discovered)
            new_count = len(chat_ids) - original_count
            if new_count > 0:
                print(f"🔍 Found {new_count} new chat IDs")
                save_chat_ids(chat_ids)
        
        if not chat_ids:
            print("❌ No chat IDs available. Please:")
            print("   1. Set TELEGRAM_CHAT_ID in config.py for exclusive mode, OR")
            print("   2. Send a message to your bot to discover chat IDs automatically")
            return
    
    print(f"\n📱 Sending {len(new_apartments)} new apartments to {len(chat_ids)} chat(s)...")
    
    total_success_count = 0
    chat_ids_to_remove = set()
    
    for chat_id in chat_ids:
        print(f"\n📤 Sending to chat ID: {chat_id}")
        success_count = 0
        
        for i, apartment in enumerate(new_apartments, 1):
            message = format_apartment_for_telegram(apartment)
            
            result = send_telegram_message(bot_token, chat_id, message)
            if result is True:
                success_count += 1
                print(f"✅ Sent apartment {i}/{len(new_apartments)} to chat {chat_id}")
            elif result == "REMOVE_CHAT_ID":
                print(f"🚫 Marking chat {chat_id} for removal due to error")
                chat_ids_to_remove.add(chat_id)
                break  # Stop sending to this chat ID
            else:
                print(f"❌ Failed to send apartment {i}/{len(new_apartments)} to chat {chat_id}")
            
            # Small delay between messages to avoid rate limiting
            import time
            time.sleep(0.5)
        
        total_success_count += success_count
        print(f"📊 Chat {chat_id}: {success_count}/{len(new_apartments)} messages sent")
    
    # Remove problematic chat IDs
    if chat_ids_to_remove:
        for chat_id in chat_ids_to_remove:
            chat_ids = remove_chat_id(chat_id, chat_ids)
    
    print(f"\n📱 Telegram export complete: {total_success_count} total messages sent to {len(chat_ids)} active chats")


def send_debug_apartment_to_telegram(apartments_list, bot_token, debug_chat_id):
    """Send the most recent apartment as a debug message to the specified chat ID"""
    if not apartments_list:
        print("📱 No apartments available for debug message")
        return
    
    if bot_token == "YOUR_BOT_TOKEN_HERE":
        print("❌ Please configure TELEGRAM_BOT_TOKEN in config.py")
        return
    
    # Check if DEBUG_CHAT is properly configured
    debug_configured = (debug_chat_id and 
                       debug_chat_id.strip() != "" and 
                       debug_chat_id not in ["YOUR_DEBUG_CHAT_ID_HERE", "YOUR_CHAT_ID_HERE", "YOUR_TELEGRAM_CHAT_ID_HERE"] and
        not debug_chat_id.startswith("YOUR_") and
        not debug_chat_id.endswith("_HERE"))
    
    if not debug_configured:
        print("📱 DEBUG_CHAT not configured, skipping debug message")
        print(f"📱 DEBUG_CHAT value received: '{debug_chat_id}'")
        return
    
    # Get the most recent apartment (first in the list, as they're usually sorted by date)
    most_recent_apartment = apartments_list[0]
    
    print(f"\n🔍 Sending DEBUG message to chat ID: {debug_chat_id}")
    print(f"🔍 Debug apartment: {most_recent_apartment['title'][:50]}...")
    
    # Format the apartment with debug flag
    debug_message = format_apartment_for_telegram(most_recent_apartment, is_debug=True)
    
    # Send the debug message
    result = send_telegram_message(bot_token, debug_chat_id, debug_message)
    
    if result is True:
        print(f"✅ DEBUG message sent successfully to chat {debug_chat_id}")
    elif result == "REMOVE_CHAT_ID":
        print(f"🚫 DEBUG chat {debug_chat_id} has issues (bot blocked, chat not found, etc.)")
    else:
        print(f"❌ Failed to send DEBUG message to chat {debug_chat_id}")


 