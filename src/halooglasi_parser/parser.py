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
        price_per_m2 = "N/A"
        price_by_surface_div = soup.find("div", class_="price-by-surface")
        if price_by_surface_div:
            price_by_surface_span = price_by_surface_div.find("span")
            if price_by_surface_span:
                price_per_m2 = price_by_surface_span.get_text().strip()
        
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
        
        # Extract area and room information from product-features
        area = "N/A"
        rooms = "N/A"
        
        product_features_ul = soup.find("ul", class_="product-features")
        if product_features_ul:
            feature_items = product_features_ul.find_all("li")
            for item in feature_items:
                value_wrapper = item.find("div", class_="value-wrapper")
                if value_wrapper:
                    text = value_wrapper.get_text().strip()
                    
                    # Extract area (look for "55 m2Kvadratura")
                    if "Kvadratura" in text:
                        area_match = re.search(r'(\d+)\s*m', text)
                        if area_match:
                            area = area_match.group(1) + "m²"
                    
                    # Extract rooms (look for "2.5 Broj soba")
                    if "Broj soba" in text:
                        room_match = re.search(r'(\d+\.?\d*)', text)
                        if room_match:
                            rooms = room_match.group(1) + " rooms"
        
        # If not found in product-features, try fallback from title
        if area == "N/A":
            area_match = re.search(r'(\d+)\s*m', title)
            area = area_match.group(1) + "m²" if area_match else "N/A"
        
        if rooms == "N/A":
            room_match = re.search(r'(\d+\.?\d*)\s*stan', title)
            rooms = room_match.group(1) + " rooms" if room_match else "N/A"
        
        # Extract location from title (usually the first part before comma)
        location_match = re.match(r'^([^,]+)', title)
        location = location_match.group(1).strip() if location_match else "N/A"
        
        # Extract agent type
        agent_span = soup.find("span", {"data-field-name": "oglasivac_nekretnine_s"})
        agent_type_raw = agent_span.get_text().strip() if agent_span else "N/A"
        
        # Translate agent type to English
        agent_type_translations = {
            "Agencija": "Agency",
            "Vlasnik": "Owner"
        }
        agent_type = agent_type_translations.get(agent_type_raw, agent_type_raw)
        
        # Extract image count (using specific class)
        img_count_span = soup.find("span", class_="pi-img-count-num")
        image_count = img_count_span.get_text().strip() + " images" if img_count_span else "N/A"
        
        # Extract price by surface info
        price_by_surface = "N/A"
        price_by_surface_div = soup.find("div", class_="price-by-surface")
        if price_by_surface_div:
            price_by_surface_span = price_by_surface_div.find("span")
            price_by_surface = price_by_surface_span.get_text().strip() if price_by_surface_span else "N/A"
        else:
            price_by_surface = "N/A"
        
        # Extract subtitle places info (ul with li items)
        subtitle_places_ul = soup.find("ul", class_="subtitle-places")
        if subtitle_places_ul:
            place_items = subtitle_places_ul.find_all("li")
            if place_items:
                places_list = [item.get_text().strip() for item in place_items if item.get_text().strip()]
                subtitle_places = " • ".join(places_list) if places_list else "N/A"
            else:
                subtitle_places = subtitle_places_ul.get_text().strip() if subtitle_places_ul.get_text().strip() else "N/A"
        else:
            subtitle_places = "N/A"
        
        # Extract product features info (ul with li items containing value-wrapper)
        product_features = "N/A"
        product_features_ul = soup.find("ul", class_="product-features")
        if product_features_ul:
            feature_items = product_features_ul.find_all("li")
            if feature_items:
                features_list = []
                for item in feature_items:
                    value_wrapper = item.find("div", class_="value-wrapper")
                    if value_wrapper:
                        # Extract the value and legend
                        value_text = value_wrapper.get_text().strip()
                        # Clean up the text by removing extra spaces
                        clean_text = re.sub(r'\s+', ' ', value_text)
                        features_list.append(clean_text)
                product_features = " • ".join(features_list) if features_list else "N/A"
            else:
                product_features = product_features_ul.get_text().strip() if product_features_ul.get_text().strip() else "N/A"
        else:
            product_features = "N/A"
        
        # Extract description from text-description-list (p tag)
        description_p = soup.find("p", class_="text-description-list")
        if description_p:
            # Get text and clean it up
            description_text = description_p.get_text().strip()
            # Replace multiple whitespaces with single space
            description = re.sub(r'\s+', ' ', description_text) if description_text else "N/A"
        else:
            description = "N/A"

        yield {
            'id': apartment_id,
            'price': price,
            'price_per_m2': price_per_m2,
            'price_by_surface': price_by_surface,
            'title': title,
            'location': location,
            'area': area,
            'rooms': rooms,
            'agent_type': agent_type,
            'image_count': image_count,
            'subtitle_places': subtitle_places,
            'product_features': product_features,
            'description': description,
            'publish_date': publish_date,
            'publish_date_str': publish_date_str,
            'link': full_link
        }
