import requests
import json
from datetime import datetime


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
        print(f"❌ Failed to send Telegram message: {e}")
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


def send_new_apartments_to_telegram(new_apartments, bot_token, chat_id):
    """Send each new apartment as a separate Telegram message"""
    if not new_apartments:
        print("📱 No new apartments to send to Telegram")
        return
    
    if bot_token == "YOUR_BOT_TOKEN_HERE" or chat_id == "YOUR_CHAT_ID_HERE":
        print("❌ Please configure TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in config.py")
        return
    
    print(f"\n📱 Sending {len(new_apartments)} new apartments to Telegram...")
    
    success_count = 0
    for i, apartment in enumerate(new_apartments, 1):
        message = format_apartment_for_telegram(apartment)
        
        if send_telegram_message(bot_token, chat_id, message):
            success_count += 1
            print(f"✅ Sent apartment {i}/{len(new_apartments)} to Telegram")
        else:
            print(f"❌ Failed to send apartment {i}/{len(new_apartments)} to Telegram")
        
        # Small delay between messages to avoid rate limiting
        import time
        time.sleep(0.5)
    
    print(f"📱 Telegram export complete: {success_count}/{len(new_apartments)} messages sent successfully")


 