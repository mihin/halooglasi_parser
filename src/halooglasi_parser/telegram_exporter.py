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
    """Format apartment data for Telegram message"""
    price = format_price(apartment['price'])
    
    # Build apartment details
    details = []
    if apartment['area'] != "N/A":
        details.append(apartment['area'])
    if apartment['rooms'] != "N/A":
        details.append(apartment['rooms'])
    if apartment['price_per_m2'] != "N/A":
        details.append(apartment['price_per_m2'])
    
    details_str = " • ".join(details) if details else "Details not available"
    
    # Add additional details if available
    additional_info = []
    if apartment['subtitle_places'] != "N/A":
        additional_info.append(f"🏘️ <b>Area:</b> {apartment['subtitle_places']}")
    if apartment['price_by_surface'] != "N/A":
        additional_info.append(f"💶 <b>Price Info:</b> {apartment['price_by_surface']}")
    if apartment['product_features'] != "N/A":
        additional_info.append(f"🏠 <b>Features:</b> {apartment['product_features']}")
    if apartment['description'] != "N/A" and len(apartment['description']) < 200:
        additional_info.append(f"📋 <b>Description:</b> {apartment['description']}")
    
    additional_text = "\n".join(additional_info)
    if additional_text:
        additional_text = "\n\n" + additional_text
    
    # Format message with HTML
    message = f"""🆕 <b>NEW APARTMENT FOUND!</b>
    
💰 <b>{price}</b>
📍 <b>Location:</b> {apartment['location']}
📐 <b>Details:</b> {details_str}
👤 <b>Agent:</b> {apartment['agent_type']}
📷 <b>Photos:</b> {apartment['image_count']}
📅 <b>Published:</b> {apartment['publish_date_str']}{additional_text}

📝 <b>Title:</b> {apartment['title']}

🔗 <a href="{apartment['link']}">View on HaloOglasi</a>"""
    
    return message


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


 