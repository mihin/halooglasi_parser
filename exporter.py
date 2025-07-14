import gspread
from openpyxl import Workbook
from collections import defaultdict
from datetime import datetime


def save_to_excel(data_generator, output_file="halooglasi_data.xlsx", max_days_old=7):
    """Write generator to xlsx file with enhanced formatting"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Ads Data"
    ws.append(["Price (€)", "Price/m²", "Location", "Area", "Rooms", "Agent", "Images", "Date", "Description", "Link"])

    # Group apartments by date and collect data
    apartments_by_date = defaultdict(list)
    total_count = 0
    
    print("\n" + "="*80)
    print("APARTMENT SEARCH RESULTS")
    print("="*80)
    
    for apartment_data in data_generator:
        total_count += 1
        
        # Group by date
        date_key = apartment_data['publish_date_str']
        apartments_by_date[date_key].append(apartment_data)
        
        # Add to Excel
        ws.append([
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
        ])
    
    # Sort dates (newest first)
    sorted_dates = sorted(apartments_by_date.keys(), key=lambda x: parse_date_for_sorting(x), reverse=True)
    
    # Display results grouped by date
    for date_str in sorted_dates:
        apartments = apartments_by_date[date_str]
        
        print(f"\n📅 {date_str} ({len(apartments)} listings)")
        print("-" * 60)
        
        for i, apt in enumerate(apartments, 1):
            print(f"\n{i}. 💰 {format_price(apt['price'])}")
            print(f"   📍 {apt['location']}")
            print(f"   📐 {apt['area']} • {apt['rooms']} • {apt['price_per_m2']}")
            print(f"   👤 {apt['agent_type']} • {apt['image_count']}")
            print(f"   📝 {apt['title']}")
            print(f"   🔗 {apt['link']}")
    
    wb.save(output_file)
    
    print(f"\n{'='*80}")
    print(f"SEARCH RESULTS SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Total found: {total_count} apartments")
    print(f"✅ Grouped by dates: {len(sorted_dates)} different dates")
    print(f"✅ Data saved to: {output_file}")
    print(f"✅ Results older than {max_days_old} days excluded")
    print(f"{'='*80}")


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
