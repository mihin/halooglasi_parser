from bs4 import BeautifulSoup
import html
import re
from datetime import datetime, timedelta


def get_info(apartments_data, base_url, max_days_old=7):
    """The function receives apartment data and extracts detailed information"""
    cutoff_date = datetime.now() - timedelta(days=max_days_old)
    
    for apartment in apartments_data:
        # Get id, url, link title
        apartment_id = apartment.get("Id", "N/A")
        relative_url = apartment.get("RelativeUrl", "N/A")
        full_link = base_url + relative_url if relative_url != "N/A" else "N/A"
        title = apartment.get("Title", "N/A")

        # Decoding HTML
        list_html = apartment.get("ListHTML", "")
        decoded_html = html.unescape(list_html)

        # Parsing ListHTML to extract detailed information
        soup = BeautifulSoup(decoded_html, "html.parser")
        
        # Extract price
        price_span = soup.find("span", {"data-value": True})
        price = int(price_span["data-value"].replace(".", "")) if price_span else "N/A"
        
        # Extract price per m²
        price_per_m2_span = soup.find("span", string=re.compile(r"€/m"))
        price_per_m2 = price_per_m2_span.get_text().strip() if price_per_m2_span else "N/A"
        
        # Extract publish date
        publish_date_span = soup.find("span", class_="publish-date")
        publish_date_str = publish_date_span.get_text().strip() if publish_date_span else "N/A"
        
        # Parse publish date and filter old results
        publish_date = None
        if publish_date_str != "N/A":
            try:
                # Parse date in format "14.07.2025."
                date_clean = publish_date_str.replace(".", "")
                publish_date = datetime.strptime(date_clean, "%d%m%Y")
                
                # Skip if older than specified days
                if publish_date < cutoff_date:
                    continue
                    
            except ValueError:
                # If date parsing fails, include the item but mark date as invalid
                publish_date_str = "Invalid date"
        
        # Extract area information
        area_match = re.search(r'(\d+)\s*m', title)
        area = area_match.group(1) + "m²" if area_match else "N/A"
        
        # Extract location from title (usually the first part before comma)
        location_match = re.match(r'^([^,]+)', title)
        location = location_match.group(1).strip() if location_match else "N/A"
        
        # Extract room information
        room_match = re.search(r'(\d+\.?\d*)\s*stan', title)
        rooms = room_match.group(1) + " rooms" if room_match else "N/A"
        
        # Extract agent type
        agent_span = soup.find("span", {"data-field-name": "oglasivac_nekretnine_s"})
        agent_type_raw = agent_span.get_text().strip() if agent_span else "N/A"
        
        # Translate agent type to English
        agent_type_translations = {
            "Agencija": "Agency",
            "Vlasnik": "Owner"
        }
        agent_type = agent_type_translations.get(agent_type_raw, agent_type_raw)
        
        # Extract image count
        img_count_span = soup.find("span", class_="pi-img-count-num")
        image_count = img_count_span.get_text().strip() + " images" if img_count_span else "N/A"

        yield {
            'id': apartment_id,
            'price': price,
            'price_per_m2': price_per_m2,
            'title': title,
            'location': location,
            'area': area,
            'rooms': rooms,
            'agent_type': agent_type,
            'image_count': image_count,
            'publish_date': publish_date,
            'publish_date_str': publish_date_str,
            'link': full_link
        }
