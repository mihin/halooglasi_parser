# Halooglasi.com Apartment Parser

This application scrapes apartment listings from https://www.halooglasi.com/ to find apartments for **purchase** in Belgrade, Serbia.

## 🏠 Current Configuration

The script is configured to search for apartments with the following criteria:

- **Type**: Apartments for **purchase** (not rent)
- **Location**: Belgrade - 51 specific areas (excludes Batajnica, Ovča, Zemun Polje, Boleč, Sremčica, Jakovo, Borča, Ledine)
- **Price Range**: €110,000 - €126,000
- **Area**: 45m² minimum
- **Rooms**: 2.0 - 4.5 rooms (4-9 in system values)
- **Floor**: PR = prizemlje/ground floor minimum
- **Legal Status**: Legally registered (uknjiženo)
- **Excludes**: Properties needing renovation

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/shestakovitch/halooglasi_parser.git
cd halooglasi_parser
```

### 2. Set Up Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### 3. Run the Script
```bash
python3 main.py
```

The script will:
- Display search criteria in the console
- Show each apartment found with ID, price, location, and link
- Save results to `halooglasi_data.xlsx` (Excel file)
- Save raw data to `halooglasi_data.json` (JSON file)

## 📊 Output Example

```
Starting apartment search...
Search criteria:
  - Price: €110000 - €126000
  - Area: 45m² minimum
  - Rooms: 4 - 9 (system values)
  - Floor: PR minimum (ground floor+)
  - Legal status: 12000004 (legally registered)
  - Location areas: 51 Belgrade areas
  - Date filter: Results from last 7 days only

Found 144 apartments matching your criteria

📅 14.07.2025. (50 oglasa)
------------------------------------------------------------

1. 💰 €121.500
   📍 Rakovica
   📐 55m² • 2.5 soba • 2.209 €/m²
   👤 Agencija • 14 slika
   📝 Rakovica, 2.5 stan, zgrada od f.cigle ID#1697
   🔗 https://www.halooglasi.com/nekretnine/prodaja-stanova/...

2. 💰 €121.500
   📍 Zvezdara
   📐 45m² • N/A • N/A
   👤 Agencija • 12 slika
   📝 Prodaja stana - Zvezdara, 45m2
   🔗 https://www.halooglasi.com/nekretnine/prodaja-stanova/...

📅 13.07.2025. (25 oglasa)
------------------------------------------------------------
...
```

## 📊 Output Example

```
Starting apartment search...
Search criteria:
  - Price: €110000 - €126000
  - Area: 45m² minimum
  - Rooms: 4 - 9 (system values)
  - Floor: PR minimum (ground floor+)
  - Legal status: 12000004 (legally registered)
  - Location areas: 51 Belgrade areas
  - Date filter: Results from last 7 days only

Found 144 apartments matching your criteria

📅 14.07.2025. (50 oglasa)
------------------------------------------------------------

1. 💰 €121.500
   📍 Rakovica
   📐 55m² • 2.5 soba • 2.209 €/m²
   👤 Agencija • 14 slika
   📝 Rakovica, 2.5 stan, zgrada od f.cigle ID#1697
   🔗 https://www.halooglasi.com/nekretnine/prodaja-stanova/...

2. 💰 €121.500
   📍 Zvezdara
   📐 45m² • N/A • N/A
   👤 Agencija • 12 slika
   📝 Prodaja stana - Zvezdara, 45m2
   🔗 https://www.halooglasi.com/nekretnine/prodaja-stanova/...

📅 13.07.2025. (25 oglasa)
------------------------------------------------------------
...
```

## 📋 Enhanced Output Features

### ✅ **What's New:**
- **🚫 Hidden IDs**: Apartment IDs are hidden for cleaner display
- **📅 Date Grouping**: Results grouped by publish date
- **📊 Rich Details**: Area, rooms, price per m², agent type, image count
- **📍 Location Extraction**: Automatic location parsing from titles
- **🎨 Visual Icons**: Emoji icons for better organization
- **📈 Statistics**: Comprehensive summary with counts and filters

### ✅ **Information Displayed:**
- **💰 Price**: Formatted with thousands separator
- **📍 Location**: Extracted from listing title
- **📐 Details**: Area, room count, price per m²
- **👤 Agent**: Agency or owner information
- **📷 Images**: Number of photos available
- **📝 Description**: Full listing title
- **🔗 Link**: Direct link to the property

### ✅ **Excel Export Enhanced:**
- **More Columns**: Price/m², Location, Area, Rooms, Agent, Images, Date
- **Better Organization**: Structured data for analysis
- **Date Sorting**: Newest listings first

## 🕒 Date Filtering

The script automatically filters results to show only recent listings:

- **Default**: Last 7 days only
- **Configurable**: Change `MAX_DAYS_OLD` variable in `main.py`
- **Automatic**: Older listings are excluded automatically
- **Grouped**: Results are grouped by publish date (newest first)

```python
# In main.py - adjust this value to change the date filter
MAX_DAYS_OLD = 7  # Show only results from last 7 days
```

## ⚙️ Configuration

### Modifying Search Criteria

Edit `config.py` to change search parameters:

```python
# Price range in euros
price_from = '110000'
price_to = '126000'

# Area in square meters
apartment_area_from = 45
apartment_area_to = None

# Number of rooms (system values: 4=2.0 rooms, 6=3.0 rooms, 8=4.0 rooms, 9=4.5 rooms)
number_of_rooms_from = '4'
number_of_rooms_to = '9'

# Floor (3 = 3rd floor minimum)
floor_from = '3'
floor_to = None
```

### Location Areas

The script searches in 51 specific Belgrade areas. To modify locations, update the `FieldValues` array in `json_data['MultiFieldORQueries']` in `config.py`.

### Legal Status Options

- `12000003`: Uknjiženo (legally registered - old code)
- `12000004`: Uknjiženo (legally registered - current code)

## 📁 Output Files

- **`halooglasi_data.xlsx`**: Enhanced Excel file with columns:
  - Price (€), Price/m², Location, Area, Rooms, Agent, Images, Date, Description, Link
- **`halooglasi_data.json`**: Raw JSON response from the API

### Excel File Structure:
| Column | Description |
|--------|-------------|
| Price (€) | Property price in euros |
| Price/m² | Price per square meter |
| Location | Extracted location from title |
| Area | Property area in m² |
| Rooms | Number of rooms |
| Agent | Agency or owner |
| Images | Number of photos |
| Date | Publish date |
| Description | Full listing title |
| Link | Direct URL to property |

## 🔧 Advanced Usage

### Google Sheets Integration (Optional)

To save results to Google Sheets instead of Excel:

1. Install gspread: Already included in requirements.txt
2. Enable API Access: https://docs.gspread.org/en/v6.1.3/oauth2.html#enable-api-access
3. Download credentials JSON file and save as `creds.json` in project root
4. Create a Google Sheet named "cityexpert_parsing_report"
5. Share the sheet with the client_email from creds.json
6. Modify `main.py`:
   ```python
   # Change this line:
   save_to_excel(parsed_data)
   # To this:
   save_to_gs(parsed_data)
   ```

### Switching Between Buy and Rent

To search for rental apartments instead:

1. Change `CategoryId` from `'1'` to `'13'` in `config.py`
2. Change `SearchTypeIds` from `[1]` to `[2, 3]`
3. Update `BaseTaxonomy` from `/nekretnine/prodaja-stanova` to `/nekretnine/izdavanje-stanova`
4. Adjust price range to rental prices (e.g., 300-800 euros)

## 📝 Notes

- The script uses the official Halooglasi.com API
- Results are sorted by most recent first
- Duplicate listings are automatically removed
- The script respects the website's rate limits
- Legal status filter ensures only properly registered properties are included

## 🛠️ For LLM Usage

To run this script programmatically:

```bash
# Activate virtual environment and run
source venv/bin/activate && python3 main.py

# Or run directly if environment is already active
python3 main.py
```

The script will output results to both console and files, making it easy to process the data programmatically.
