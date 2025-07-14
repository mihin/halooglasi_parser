from config import base_url, cookies, headers, json_data
from scraper import fetch_data
from parser import get_info
from exporter import save_to_gs, save_to_excel


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
    print("\nFetching data...")

    # Getting the data
    apartments_data = fetch_data(url, cookies, headers, json_data)

    if not apartments_data:
        print("ERROR: No data received from the API")
        return

    # Processing the data
    data = apartments_data.get("Ads", [])
    print(f"Raw data received: {len(data)} apartments")
    
    if not data:
        print("WARNING: No apartments found in the response")
        print("Full response structure:")
        print(apartments_data.keys())
        return

    parsed_data = get_info(data, base_url)
    parsed_list = list(parsed_data)
    
    print(f"Parsed data: {len(parsed_list)} apartments")
    
    if not parsed_list:
        print("WARNING: No apartments after parsing")
        return

    # save_to_gs(parsed_list) # If you want to save result to Google Drive
    result_count = save_to_excel(parsed_list) # If you want to save result to your computer
    
    if result_count == 0:
        print("\nNo apartments found matching your criteria. Consider:")
        print("1. Expanding the price range")
        print("2. Reducing minimum area requirement")
        print("3. Including more location areas")
        print("4. Checking if the search parameters are correct")


if __name__ == "__main__":
    main()
