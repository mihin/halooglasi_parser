from bs4 import BeautifulSoup
import html


def get_info(apartments_data, base_url):
    """The function receives apartment data"""
    for apartment in apartments_data:
        # Get id, url, link title
        apartment_id = apartment.get("Id", "N/A")
        relative_url = apartment.get("RelativeUrl", "N/A")
        full_link = base_url + relative_url if relative_url != "N/A" else "N/A"
        title = apartment.get("Title", "N/A")

        # Decoding HTML
        list_html = apartment.get("ListHTML", "")
        decoded_html = html.unescape(list_html)

        # Parsing ListHTML to extract price value
        soup = BeautifulSoup(decoded_html, "html.parser")
        span = soup.find("span", {"data-value": True})
        price = int(span["data-value"].replace(".", "")) if span else "N/A"

        yield apartment_id, price, title, full_link
