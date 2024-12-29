from config import base_url, cookies, headers, json_data
from scraper import fetch_data
from parser import get_info
from exporter import save_to_gs, save_to_excel


def main():
    url = "https://www.halooglasi.com/Quiddita.Widgets.Ad/AdCategoryBasicSearchWidgetAux/GetSidebarData"

    # Getting the data
    apartments_data = fetch_data(url, cookies, headers, json_data)

    # Processing the data
    data = apartments_data.get("Ads", [])
    parsed_data = get_info(data, base_url)


    # save_to_gs(parsed_data) # If you want to save result to Google Drive
    save_to_excel(parsed_data) # If you want to save result to your computer


if __name__ == "__main__":
    main()
