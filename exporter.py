import gspread
import pandas as pd
from openpyxl import Workbook


def save_to_gs(generator):
    columns = ["Apartment ID", "Price", "Description", "Link"]
    df = pd.DataFrame(generator, columns=columns)

    gc = gspread.service_account(filename="creds.json")

    # Open a sheet from a spreadsheet in one go
    file_name = "halooglasi_parsing_report"
    wks = gc.open(file_name).sheet1

    wks.update([df.columns.values.tolist()] + df.values.tolist())
    wks.format('A1:D1', {'textFormat': {'bold': True}})
    print(f"Data saved to the file {file_name} in your Google Drive")


def save_to_excel(data_generator, output_file="halooglasi_data.xlsx"):
    """Write generator to xlsx file"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Ads Data"
    ws.append(["Id", "Cost in euros", "Description", "Link"])  # Column headers

    # Set for storing unique Id's
    ids_set = set()
    count = 0

    print("\n" + "="*80)
    print("APARTMENT SEARCH RESULTS")
    print("="*80)
    
    for row in data_generator:
        apartment_id = row[0]
        if apartment_id in ids_set:
            continue  # Skip duplicate Ids
        ids_set.add(apartment_id)  # Adding Id to the set
        ws.append(row)  # Adding a row to xlsx file
        count += 1
        
        # Print each result to console
        print(f"\n{count}. ID: {row[0]}")
        print(f"   Price: {row[1]}")
        print(f"   Description: {row[2][:100]}..." if len(row[2]) > 100 else f"   Description: {row[2]}")
        print(f"   Link: {row[3]}")

    wb.save(output_file)
    
    print("\n" + "="*80)
    print(f"SUMMARY: Found {count} apartments matching your criteria")
    print(f"Data saved to the file {output_file} on your computer")
    print("="*80)

    return count
