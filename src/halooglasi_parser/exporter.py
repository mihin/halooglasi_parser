import gspread
import os
from openpyxl import Workbook
from collections import defaultdict
from datetime import datetime


def display_apartments_to_console(new_apartments, existing_apartments, max_days_old=7):
    """Display apartments to console with enhanced formatting"""
    # Group apartments by date and collect data
    new_apartments_by_date = defaultdict(list)
    existing_apartments_by_date = defaultdict(list)
    total_count = 0
    
    print("\n" + "="*80)
    print("APARTMENT SEARCH RESULTS")
    print("="*80)
    
    # Process new apartments
    for apartment_data in new_apartments:
        total_count += 1
        date_key = apartment_data['publish_date_str']
        new_apartments_by_date[date_key].append(apartment_data)
    
    # Process existing apartments
    for apartment_data in existing_apartments:
        total_count += 1
        date_key = apartment_data['publish_date_str']
        existing_apartments_by_date[date_key].append(apartment_data)
    
    # Display NEW apartments first
    if new_apartments_by_date:
        print(f"\n🆕 NEW APARTMENTS ({len(new_apartments)} total)")
        print("=" * 80)
        sorted_new_dates = sorted(new_apartments_by_date.keys(), key=lambda x: parse_date_for_sorting(x), reverse=True)
        
        for date_str in sorted_new_dates:
            apartments = new_apartments_by_date[date_str]
            print(f"\n📅 {date_str} ({len(apartments)} new listings)")
            print("-" * 60)
            
            for i, apt in enumerate(apartments, 1):
                # Title, Price, Price/m²
                print(f"\n{i}. 📝 {apt['title']}")
                print(f"   💰 {format_price(apt['price'])} • {apt['price_per_m2']} 🆕")
                
                # Location
                if apt['subtitle_places'] != "N/A":
                    print(f"   🏘️  {apt['subtitle_places']}")
                
                # Link
                print(f"   🔗 {apt['link']}")
                
                # All other details
                if apt['product_features'] != "N/A":
                    # Remove "Kvadratura" from product features
                    features_clean = apt['product_features'].replace('Kvadratura', '').replace('  ', ' ').strip()
                    print(f"   🏠 {features_clean}")
                
                # Description
                if apt['description'] != "N/A":
                    print(f"   📋 {apt['description']}")
                
                # Agent info at the end
                print(f"   👤 {apt['agent_type']} • {apt['image_count']}")
    
    # Display EXISTING apartments second
    if existing_apartments_by_date:
        print(f"\n📋 PREVIOUSLY SEEN APARTMENTS ({len(existing_apartments)} total)")
        print("=" * 80)
        sorted_existing_dates = sorted(existing_apartments_by_date.keys(), key=lambda x: parse_date_for_sorting(x), reverse=True)
        
        for date_str in sorted_existing_dates:
            apartments = existing_apartments_by_date[date_str]
            print(f"\n📅 {date_str} ({len(apartments)} existing listings)")
            print("-" * 60)
            
            for i, apt in enumerate(apartments, 1):
                # Title, Price, Price/m²
                print(f"\n{i}. 📝 {apt['title']}")
                print(f"   💰 {format_price(apt['price'])} • {apt['price_per_m2']}")
                
                # Location
                if apt['subtitle_places'] != "N/A":
                    print(f"   🏘️  {apt['subtitle_places']}")
                
                # Link
                print(f"   🔗 {apt['link']}")
                
                # All other details
                if apt['product_features'] != "N/A":
                    # Remove "Kvadratura" from product features
                    features_clean = apt['product_features'].replace('Kvadratura', '').replace('  ', ' ').strip()
                    print(f"   🏠 {features_clean}")
                
                # Description
                if apt['description'] != "N/A":
                    print(f"   📋 {apt['description']}")
                
                # Agent info at the end
                print(f"   👤 {apt['agent_type']} • {apt['image_count']}")
    
    print(f"\n{'='*80}")
    print(f"SEARCH RESULTS SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Total found: {total_count} apartments")
    print(f"🆕 New apartments: {len(new_apartments)}")
    print(f"📋 Previously seen: {len(existing_apartments)}")
    print(f"✅ New dates: {len(new_apartments_by_date)} different dates")
    print(f"✅ Existing dates: {len(existing_apartments_by_date)} different dates")
    print(f"✅ Results older than {max_days_old} days excluded")
    print(f"{'='*80}")


def save_to_excel(new_apartments, existing_apartments, output_file=None, max_days_old=7):
    if output_file is None:
        # Get the project root directory (two levels up from this file)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        data_dir = os.path.join(project_root, "data")
        output_file = os.path.join(data_dir, "halooglasi_data.xlsx")
    """Write apartments to xlsx file with enhanced formatting"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Ads Data"
    ws.append(["Status", "Price (€)", "Price/m²", "Price by Surface", "Location", "Subtitle Places", "Area", "Rooms", "Agent", "Images", "Product Features", "Description", "Full Description", "Date", "Title", "Link"])

    total_count = 0
    
    # Process new apartments
    for apartment_data in new_apartments:
        total_count += 1
        # Add to Excel with "NEW" status
        ws.append([
            "NEW",
            apartment_data['price'],
            apartment_data['price_per_m2'],
            apartment_data['price_by_surface'],
            apartment_data['location'],
            apartment_data['subtitle_places'],
            apartment_data['area'],
            apartment_data['rooms'],
            apartment_data['agent_type'],
            apartment_data['image_count'],
            apartment_data['product_features'],
            apartment_data['description'],
            apartment_data['title'],
            apartment_data['publish_date_str'],
            apartment_data['title'],
            apartment_data['link']
        ])
    
    # Process existing apartments
    for apartment_data in existing_apartments:
        total_count += 1
        # Add to Excel with "EXISTING" status
        ws.append([
            "EXISTING",
            apartment_data['price'],
            apartment_data['price_per_m2'],
            apartment_data['price_by_surface'],
            apartment_data['location'],
            apartment_data['subtitle_places'],
            apartment_data['area'],
            apartment_data['rooms'],
            apartment_data['agent_type'],
            apartment_data['image_count'],
            apartment_data['product_features'],
            apartment_data['description'],
            apartment_data['title'],
            apartment_data['publish_date_str'],
            apartment_data['title'],
            apartment_data['link']
        ])
    
    wb.save(output_file)
    print(f"✅ Excel data saved to: {output_file}")


def parse_date_for_sorting(date_str):
    """Parse date string for sorting purposes"""
    if date_str == "N/A" or date_str == "Invalid date":
        return datetime.min
    try:
        date_clean = date_str.replace(".", "")
        return datetime.strptime(date_clean, "%d%m%Y")
    except ValueError:
        return datetime.min


def format_price(price):
    """Format price with thousands separator"""
    if price == "N/A":
        return "N/A"
    return f"€{price:,}".replace(",", ".")


def save_to_gs(data_generator):
    """Save data to Google Sheets"""
    import gspread
    
    gc = gspread.service_account(filename="creds.json")
    sh = gc.open("cityexpert_parsing_report")
    worksheet = sh.sheet1
    
    # Clear existing data
    worksheet.clear()
    
    # Add headers
    headers = ["Price (€)", "Price/m²", "Location", "Area", "Rooms", "Agent", "Images", "Date", "Description", "Link"]
    worksheet.append_row(headers)
    
    # Add data
    for apartment_data in data_generator:
        row = [
            apartment_data['price'],
            apartment_data['price_per_m2'],
            apartment_data['location'],
            apartment_data['area'],
            apartment_data['rooms'],
            apartment_data['agent_type'],
            apartment_data['image_count'],
            apartment_data['publish_date_str'],
            apartment_data['title'],
            apartment_data['link']
        ]
        worksheet.append_row(row)
    
    print("Data successfully saved to Google Sheets!")
