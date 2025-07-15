import fake_user_agent

user = fake_user_agent.user_agent()

base_url = "https://www.halooglasi.com"

# Variables for filtering - BUYING APARTMENTS (BASED ON PROVIDED URL)
# Cost in euros (buying price range)
price_from = '110000'
price_to = '126000'

# Apartment area (minimum 45m²)
apartment_area_from = 45
apartment_area_to = None

# Number of rooms (4-9 in system values = 2.0-4.5 rooms)
number_of_rooms_from = '4'
number_of_rooms_to = '9'

# Floor (PR = prizemlje/ground floor minimum)
floor_from = 'PR'
floor_to = None

cookies = {
    'ASP.NET_SessionId': 'ta3nxveegc5pj322ud3amy5t',
    '_gcl_au': '1.1.94090009.1734454042',
    '_hjSessionUser_615092': 'eyJpZCI6IjQwYWRiY2I0LTZmN2UtNWNhZS1hMWQ4LWM1OWJiYjEwYWEwZSIsImNyZWF0ZWQiOjE3MzQ0NTQwNDQxNTQsImV4aXN0aW5nIjp0cnVlfQ==',
    'cookiePolicyConfirmation': 'true',
    '_gid': 'GA1.2.3149787.1734954143',
    '__gfp_64b': 'wwzVFkakvV2ghBm9CiRhgUUPx4k3myMQWZPO0tD6fE3.h7|1734454042|2|||8,2,32',
    '_hjSession_615092': 'eyJpZCI6ImNmZjFlYzZjLWQ2M2UtNGVlNS04NjFlLTdmODViZThhZjMzYiIsImMiOjE3MzQ5NjE2Mzg2NTksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
    '_gat': '1',
    '_dc_gtm_UA-4090358-9': '1',
    '_ga_TWCNL05EK4': 'GS1.1.1734961637.8.1.1734963251.17.0.0',
    '_ga': 'GA1.1.581282287.1734454042',
    '_ga_81XFKQEL79': 'GS1.2.1734961637.6.1.1734963251.24.0.0',
    '_ga_TPG5HZ7P2L': 'GS1.2.1734961637.6.1.1734963251.24.0.0',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json; charset=UTF-8',
    'origin': 'https://www.halooglasi.com',
    'priority': 'u=1, i',
    'referer': 'https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': user,
    'x-requested-with': 'XMLHttpRequest',
}

json_data = {
    'RangeQueries': [
        {
            'UnitId': 4,
            'FieldName': 'defaultunit_cena_d',
            'From': price_from,
            'To': price_to,
            'IncludeEmpty': False,
            '_min': None,
            '_max': None,
        },
        {
            'UnitId': 1,
            'FieldName': 'defaultunit_kvadratura_d',
            'From': apartment_area_from,
            'To': apartment_area_to,
            'IncludeEmpty': False,
            '_min': None,
            '_max': None,
        },
        {
            'FieldName': 'broj_soba_order_i',
            'From': number_of_rooms_from,
            'To': number_of_rooms_to,
            'IncludeEmpty': False,
        },
        {
            'FieldName': 'sprat_order_i',
            'From': floor_from,
            'To': floor_to,
            'IncludeEmpty': False,
        },
    ],
    'MultiFieldORQueries': [
        {
            'FieldName': 'grad_id_l-lokacija_id_l-mikrolokacija_id_l',
            'FieldValues': [
                # Exact location IDs from the provided URL
                40381, 40574, 40769, 40772, 40776, 40783, 40784, 40787, 40788,
                51647, 51976, 52240, 52308, 53662, 54308, 55007, 55896, 56358,
                56515, 56947, 57320, 57841, 58352, 58768, 58822, 346980, 346982,
                346983, 346984, 346985, 346986, 525616, 527587, 529392, 534654,
                534688, 534724, 534760, 534905, 534906, 534908, 537335, 538004,
                538005, 538104, 538106, 538174, 538231, 538995, 539012, 539017
            ],
        },
    ],
    'FieldQueries': [],
    'FieldORQueries': [
        {
            'FieldName': 'CategoryIds',
            'FieldValues': [
                '1',  # Buy apartments
            ],
        },
        {
            'FieldName': 'dodatno_id_ls',
            'FieldValues': [
                '12000004',  # Legal status from URL (different from previous 12000003)
            ],
        },
    ],
    'HasValueQueries': [],
    'GeoPolygonQuery': {},
    'GeoCircleQuery': {},
    'CategoryId': '1',
    'SearchTypeIds': [
        1,
    ],
    'SortFields': [
        {
            'FieldName': 'ValidFromForDisplay',
            'Ascending': False,
        },
    ],
    'GetAllGeolocations': True,
    'ItemsPerPage': 20,
    'PageNumber': 1,
    'IsGrid': False,
    'fetchBanners': False,
    'QuasiTaxonomy': '',
    'BaseTaxonomy': '/nekretnine/prodaja-stanova',
    'RenderSEOWidget': True,
    'ExcludeFieldORQueries': [
        {
            'FieldName': 'stanje_objekta_id_l',
            'FieldValues': [
                '387236',  # Za renoviranje (needs renovation)
            ],
        },
    ],
}

# Import configuration loader for credentials
from .config_loader import config_loader

# Telegram Bot Configuration
# These values are loaded from config.properties file or environment variables
# To get these values:
# 1. Create a bot with @BotFather on Telegram
# 2. Get the bot token from @BotFather  
# 3. Get your chat ID by messaging @userinfobot
# 4. Copy config.properties.template to config.properties and update values
TELEGRAM_BOT_TOKEN = config_loader.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = config_loader.get("TELEGRAM_CHAT_ID")
