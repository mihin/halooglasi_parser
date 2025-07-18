import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from halooglasi_parser.config import base_url, cookies, headers, json_data, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, DEBUG_CHAT
from halooglasi_parser.config_loader import config_loader
from halooglasi_parser.scraper import fetch_data
from halooglasi_parser.parser import get_info
from halooglasi_parser.exporter import save_to_gs, save_to_excel, display_apartments_to_console
from halooglasi_parser.id_manager import load_previous_ids, save_current_ids, get_new_apartments, get_all_ids_from_apartments
from halooglasi_parser.telegram_exporter import send_new_apartments_to_telegram, send_debug_apartment_to_telegram
import json

# Configuration: Number of days to include in results (older results will be filtered out)
MAX_DAYS_OLD = 2

# Configuration: Export to Excel file (set to True if you want Excel output)
EXPORT_TO_EXCEL = False

# Configuration: Export to Telegram bot (set to True to send new listings to Telegram)
EXPORT_TO_TELEGRAM = True


def create_result_indicators(telegram_result, new_apartments):
    """Create result indicator files for GitHub Actions workflow decisions"""
    try:
        os.makedirs("data", exist_ok=True)
        
        # Create Telegram result indicator
        with open("data/telegram_result.json", "w") as f:
            json.dump({
                "messages_sent": telegram_result.get("messages_sent", 0),
                "chats_found": telegram_result.get("chats_found", 0),
                "success": telegram_result.get("success", False),
                "new_apartments_count": len(new_apartments)
            }, f, indent=2)
        
        print(f"\n📋 Telegram result: {telegram_result.get('messages_sent', 0)} messages sent to {telegram_result.get('chats_found', 0)} chats")
        print(f"📋 Result indicator saved to data/telegram_result.json")
        
    except Exception as e:
        print(f"❌ Error creating result indicators: {e}")


def main():
    url = "https://www.halooglasi.com/Quiddita.Widgets.Ad/AdCategoryBasicSearchWidgetAux/GetSidebarData"

    print("Starting apartment search...")
    print(f"Search URL: {url}")
    print(f"Search criteria:")
    print(f"  - Price: €{json_data['RangeQueries'][0]['From']} - €{json_data['RangeQueries'][0]['To']}")
    print(f"  - Area: {json_data['RangeQueries'][1]['From']}m² minimum")
    print(f"  - Rooms: {json_data['RangeQueries'][2]['From']} - {json_data['RangeQueries'][2]['To']} (system values)")
    print(f"  - Floor: {json_data['RangeQueries'][3]['From']} minimum (ground floor+)")
    print(f"  - Category: {json_data['CategoryId']} (1=buy, 13=rent)")
    print(f"  - Legal status: {json_data['FieldORQueries'][1]['FieldValues'][0]} (12000004)")
    print(f"  - Location areas: {len(json_data['MultiFieldORQueries'][0]['FieldValues'])} Belgrade areas")
    print(f"  - Date filter: Results from last {MAX_DAYS_OLD} days only")
    
    # Show configuration sources
    config_loader.print_config_summary()
    
    # Load previously seen apartment IDs
    print("\n📋 Loading previous apartment IDs...")
    previous_ids = load_previous_ids()
    print(f"📋 Found {len(previous_ids)} previously seen apartment IDs")
    
    print("\nFetching data...")

    # Getting the data
    apartments_data = fetch_data(url, cookies, headers, json_data)

    if not apartments_data:
        print("ERROR: No data received from the API")
        return

    raw_count = len(apartments_data)
    print(f"Raw data received: {raw_count} apartments")

    # Parse the data with date filtering
    parsed_data = get_info(apartments_data, base_url, max_days_old=MAX_DAYS_OLD)

    # Convert generator to list to get count and preserve data
    apartments_list = list(parsed_data)
    filtered_count = len(apartments_list)
    
    print(f"Filtered data (last {MAX_DAYS_OLD} days): {filtered_count} apartments")
    
    if filtered_count == 0:
        print(f"\n⚠️  No apartments found within the last {MAX_DAYS_OLD} days.")
        print("Try increasing MAX_DAYS_OLD in run_search.py or check if there are new listings.")
        
        # Check if DEBUG_CHAT is configured to send debug message with most recent apartment
        if EXPORT_TO_TELEGRAM:
            print(f"\n📱 No apartments found - checking DEBUG_CHAT configuration...")
            print(f"🔍 DEBUG_CHAT value: '{DEBUG_CHAT}'")
            
            # Check if DEBUG_CHAT is properly configured (not empty, None, or placeholder)
            debug_configured = (DEBUG_CHAT and 
                              DEBUG_CHAT.strip() != "" and 
                              DEBUG_CHAT not in ["YOUR_DEBUG_CHAT_ID_HERE", "YOUR_CHAT_ID_HERE", "YOUR_TELEGRAM_CHAT_ID_HERE"] and
                              not DEBUG_CHAT.startswith("YOUR_") and
                              not DEBUG_CHAT.endswith("_HERE"))
            
            if debug_configured:
                print(f"🔍 DEBUG_CHAT configured - attempting to send DEBUG message to {DEBUG_CHAT}")
                # We need to get some apartments for debug, so let's expand the date range temporarily
                print(f"🔍 Fetching recent apartments for debug message (expanding to 7 days)...")
                debug_data = get_info(apartments_data, base_url, max_days_old=7)
                debug_apartments_list = list(debug_data)
                
                if debug_apartments_list:
                    print(f"🔍 Found {len(debug_apartments_list)} recent apartments for debug")
                    send_debug_apartment_to_telegram(debug_apartments_list, TELEGRAM_BOT_TOKEN, DEBUG_CHAT)
                else:
                    print(f"🔍 No recent apartments found even with expanded range for debug message")
            else:
                print(f"🔍 DEBUG_CHAT not configured or empty - skipping debug message")
                print(f"📱 To enable debug messages, set DEBUG_CHAT environment variable to your chat ID")
        
        return

    # Separate new and existing apartments
    print(f"\n🔍 Analyzing apartment IDs...")
    new_apartments, existing_apartments = get_new_apartments(apartments_list, previous_ids)
    
    print(f"🆕 New apartments found: {len(new_apartments)}")
    print(f"📋 Previously seen apartments: {len(existing_apartments)}")

    # Display all apartments to console
    display_apartments_to_console(new_apartments, existing_apartments, max_days_old=MAX_DAYS_OLD)

    # Export new apartments to Telegram
    telegram_result = {"messages_sent": 0, "chats_found": 0, "success": False}
    
    if EXPORT_TO_TELEGRAM:
        if new_apartments:
            # Send new apartments normally
            telegram_result = send_new_apartments_to_telegram(new_apartments, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        else:
            # No new apartments found, check if debug mode is enabled
            print(f"\n📱 No new apartments found - checking DEBUG_CHAT configuration...")
            print(f"🔍 DEBUG_CHAT value: '{DEBUG_CHAT}'")
            
            # Check if DEBUG_CHAT is properly configured (not empty, None, or placeholder)
            debug_configured = (DEBUG_CHAT and 
                              DEBUG_CHAT.strip() != "" and 
                              DEBUG_CHAT not in ["YOUR_DEBUG_CHAT_ID_HERE", "YOUR_CHAT_ID_HERE", "YOUR_TELEGRAM_CHAT_ID_HERE"] and
                              not DEBUG_CHAT.startswith("YOUR_") and
                              not DEBUG_CHAT.endswith("_HERE"))
            
            if debug_configured:
                print(f"🔍 DEBUG_CHAT configured - sending DEBUG message to {DEBUG_CHAT}")
                telegram_result = send_debug_apartment_to_telegram(apartments_list, TELEGRAM_BOT_TOKEN, DEBUG_CHAT)
            else:
                print(f"🔍 DEBUG_CHAT not configured or empty - skipping debug message")
                print(f"📱 To enable debug messages, set DEBUG_CHAT environment variable to your chat ID")
    else:
        print(f"📱 Telegram export disabled (set EXPORT_TO_TELEGRAM=True to enable)")
    
    # Create result indicators for workflow decisions
    create_result_indicators(telegram_result, new_apartments)
    
    # Save current apartment IDs for next run - only save if no new apartments or if messages were sent
    should_save_ids = len(new_apartments) == 0 or telegram_result.get("success", False)
    
    if should_save_ids:
        current_ids = get_all_ids_from_apartments(apartments_list)
        all_ids = previous_ids.union(current_ids)
        save_current_ids(all_ids)
        print(f"📋 Apartment IDs saved - Messages sent successfully: {telegram_result.get('success', False)}")
    else:
        print(f"📋 Apartment IDs NOT saved - No messages were sent to Telegram")
        print(f"📋 This prevents marking apartments as 'seen' when notifications failed")

    # Save the data
    if EXPORT_TO_EXCEL:
        save_to_excel(new_apartments, existing_apartments, max_days_old=MAX_DAYS_OLD)
    else:
        print(f"📊 Excel export disabled (set EXPORT_TO_EXCEL=True to enable)")
    
    # save_to_gs(iter(apartments_list))  # Uncomment if you want to save to Google Sheets


if __name__ == "__main__":
    main()
