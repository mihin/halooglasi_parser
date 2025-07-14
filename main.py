from config import base_url, cookies, headers, json_data
from scraper import fetch_data
from parser import get_info
from exporter import save_to_gs, save_to_excel

# Configuration: Number of days to include in results (older results will be filtered out)
MAX_DAYS_OLD = 7


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

    # Save the data (convert back to generator)
    save_to_excel(iter(apartments_list))
    # save_to_gs(iter(apartments_list))  # Uncomment if you want to save to Google Sheets


if __name__ == "__main__":
    main()
