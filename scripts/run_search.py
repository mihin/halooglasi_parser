import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from halooglasi_parser.config import base_url, cookies, headers, json_data, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from halooglasi_parser.scraper import fetch_data
from halooglasi_parser.parser import get_info
from halooglasi_parser.exporter import save_to_gs, save_to_excel, display_apartments_to_console
from halooglasi_parser.id_manager import load_previous_ids, save_current_ids, get_new_apartments, get_all_ids_from_apartments
from halooglasi_parser.telegram_exporter import send_new_apartments_to_telegram

# Configuration: Number of days to include in results (older results will be filtered out)
MAX_DAYS_OLD = 4

# Configuration: Export to Excel file (set to True if you want Excel output)
EXPORT_TO_EXCEL = False

# Configuration: Export to Telegram bot (set to True to send new listings to Telegram)
EXPORT_TO_TELEGRAM = True


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
        print("Try increasing MAX_DAYS_OLD in main.py or check if there are new listings.")
        return

    # Separate new and existing apartments
    print(f"\n🔍 Analyzing apartment IDs...")
    new_apartments, existing_apartments = get_new_apartments(apartments_list, previous_ids)
    
    print(f"🆕 New apartments found: {len(new_apartments)}")
    print(f"📋 Previously seen apartments: {len(existing_apartments)}")
    
    # Save current apartment IDs for next run
    current_ids = get_all_ids_from_apartments(apartments_list)
    all_ids = previous_ids.union(current_ids)
    save_current_ids(all_ids)

    # Display all apartments to console
    display_apartments_to_console(new_apartments, existing_apartments, max_days_old=MAX_DAYS_OLD)

    # Export new apartments to Telegram
    if EXPORT_TO_TELEGRAM:
        send_new_apartments_to_telegram(new_apartments, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
    else:
        print(f"📱 Telegram export disabled (set EXPORT_TO_TELEGRAM=True to enable)")

    # Save the data
    if EXPORT_TO_EXCEL:
        save_to_excel(new_apartments, existing_apartments, max_days_old=MAX_DAYS_OLD)
    else:
        print(f"📊 Excel export disabled (set EXPORT_TO_EXCEL=True to enable)")
    
    # save_to_gs(iter(apartments_list))  # Uncomment if you want to save to Google Sheets


if __name__ == "__main__":
    main()
