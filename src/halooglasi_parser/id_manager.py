import json
import os
from datetime import datetime

# Get the project root directory (two levels up from this file)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
ID_FILE = os.path.join(DATA_DIR, "previous_apartment_ids.json")

def load_previous_ids():
    """Load previously found apartment IDs from local file"""
    if not os.path.exists(ID_FILE):
        return set()
    
    try:
        with open(ID_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Handle both old format (plain list) and new format (dict with 'ids' key)
            if isinstance(data, list):
                # Old format: plain list of IDs
                print("📝 Converting old ID format to new format...")
                return set(data)
            elif isinstance(data, dict):
                # New format: dict with 'ids', 'last_updated', etc.
                return set(data.get('ids', []))
            else:
                print(f"⚠️  Warning: Unexpected data format in {ID_FILE}, starting with empty ID list")
                return set()
                
    except (json.JSONDecodeError, KeyError) as e:
        print(f"⚠️  Warning: Could not read {ID_FILE}: {e}, starting with empty ID list")
        return set()

def save_current_ids(apartment_ids):
    """Save current apartment IDs to local file with timestamp"""
    data = {
        'ids': list(apartment_ids),
        'last_updated': datetime.now().isoformat(),
        'count': len(apartment_ids)
    }
    
    try:
        with open(ID_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 Saved {len(apartment_ids)} apartment IDs to {ID_FILE}")
    except Exception as e:
        print(f"⚠️  Warning: Could not save IDs to {ID_FILE}: {e}")

def get_new_apartments(apartments_list, previous_ids):
    """Separate apartments into new and existing based on previous IDs"""
    new_apartments = []
    existing_apartments = []
    
    for apartment in apartments_list:
        apartment_id = str(apartment.get('id', ''))
        if apartment_id and apartment_id not in previous_ids:
            new_apartments.append(apartment)
        else:
            existing_apartments.append(apartment)
    
    return new_apartments, existing_apartments

def get_all_ids_from_apartments(apartments_list):
    """Extract all apartment IDs from the apartments list"""
    return {str(apartment.get('id', '')) for apartment in apartments_list if apartment.get('id')} 