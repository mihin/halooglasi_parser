import requests
import json
from datetime import datetime


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
            chat_ids.add(chat_id)
    
    # Convert to list and filter out empty results
    active_chat_ids = list(chat_ids)
    
    if active_chat_ids:
        print(f"📋 Found {len(active_chat_ids)} active chat(s): {active_chat_ids}")
    else:
        print("⚠️ No active chats found in recent updates")
    
    return active_chat_ids


def send_telegram_message(bot_token, chat_id, message, parse_mode="HTML"):
    """Send a message to Telegram bot"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": False
    }
    
    try:
        response = requests.post(url, data=data, timeout=30)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send Telegram message to chat {chat_id}: {e}")
        return False


def format_apartment_for_telegram(apartment):
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
    
    # 1. Title, Price, Price/m² 
    message_parts.append(f"📝 <b>{apartment['title']}</b>")
    message_parts.append(f"💰 <b>{price} • {apartment['price_per_m2']}</b> 🆕")
    
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
    
    return "\n".join(message_parts)


def format_price(price):
    """Format price with thousands separator"""
    if price == "N/A":
        return "N/A"
    return f"€{price:,}".replace(",", ".")


def send_new_apartments_to_telegram(new_apartments, bot_token, fallback_chat_id=None):
    """Send each new apartment as a separate Telegram message to all active chats"""
    if not new_apartments:
        print("📱 No new apartments to send to Telegram")
        return
    
    if bot_token == "YOUR_BOT_TOKEN_HERE":
        print("❌ Please configure TELEGRAM_BOT_TOKEN in config.py")
        return
    
    # Get all active chat IDs
    active_chat_ids = get_active_chat_ids(bot_token)
    
    # If no active chats found and we have a fallback, use it
    if not active_chat_ids and fallback_chat_id and fallback_chat_id != "YOUR_CHAT_ID_HERE":
        print(f"⚠️ No active chats found, using fallback chat ID: {fallback_chat_id}")
        active_chat_ids = [fallback_chat_id]
    
    if not active_chat_ids:
        print("❌ No chat IDs available for sending messages")
        return
    
    print(f"\n📱 Sending {len(new_apartments)} new apartments to {len(active_chat_ids)} Telegram chat(s)...")
    
    total_success_count = 0
    for chat_id in active_chat_ids:
        chat_success_count = 0
        print(f"\n🎯 Sending to chat {chat_id}...")
        
        for i, apartment in enumerate(new_apartments, 1):
            message = format_apartment_for_telegram(apartment)
            
            if send_telegram_message(bot_token, chat_id, message):
                chat_success_count += 1
                print(f"✅ Sent apartment {i}/{len(new_apartments)} to chat {chat_id}")
            else:
                print(f"❌ Failed to send apartment {i}/{len(new_apartments)} to chat {chat_id}")
            
            # Small delay between messages to avoid rate limiting
            import time
            time.sleep(0.5)
        
        total_success_count += chat_success_count
        print(f"📱 Chat {chat_id}: {chat_success_count}/{len(new_apartments)} messages sent successfully")
    
    avg_success_rate = total_success_count / (len(active_chat_ids) * len(new_apartments)) * 100 if active_chat_ids else 0
    print(f"📱 Overall Telegram export complete: {total_success_count}/{len(active_chat_ids) * len(new_apartments)} total messages sent ({avg_success_rate:.1f}% success rate)")


 