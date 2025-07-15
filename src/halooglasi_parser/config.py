import fake_user_agent

user = fake_user_agent.user_agent()

base_url = "https://www.halooglasi.com"

# Import configuration loader for credentials and filters
from .config_loader import config_loader

# Search Type Configuration
# 'buy' = buying apartments, 'rent' = renting apartments
search_type = config_loader.get("SEARCH_TYPE", "buy")

# Cost in euros
price_from = config_loader.get("PRICE_FROM", '110000')
price_to = config_loader.get("PRICE_TO", '126000')

# Apartment area in m²
apartment_area_from = int(config_loader.get("APARTMENT_AREA_FROM", '45'))
apartment_area_to = int(config_loader.get("APARTMENT_AREA_TO", '0')) if config_loader.get("APARTMENT_AREA_TO") else None

# Number of rooms (4-9 equals 2.0-4.5 rooms)
number_of_rooms_from = config_loader.get("NUMBER_OF_ROOMS_FROM", '4')
number_of_rooms_to = config_loader.get("NUMBER_OF_ROOMS_TO", '9')

# Floor (PR = prizemlje/ground floor minimum, empty = any floor)
floor_from = config_loader.get("FLOOR_FROM", 'PR')
floor_to = config_loader.get("FLOOR_TO") if config_loader.get("FLOOR_TO") else None

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
                # Belgrade location IDs - comprehensive neighborhood coverage (252 locations)
                # Covers major residential areas with detailed micro-location specificity
                
                # Major Belgrade Districts & Central Areas
                40772,   # Palilula (central part) - around Tašmajdan Park
                40776,   # Dorćol - historic riverside neighborhood
                40784,   # Kalemegdan - fortress and park area
                346980,  # Čukarica - includes Banovo Brdo, Žarkovo
                346982,  # Rakovica - includes Miljakovac, Petlovo Brdo  
                346983,  # Voždovac - includes Autokomanda, Banjica
                346984,  # Zvezdara - includes Mirijevo, Konjarnik
                346985,  # Zemun - former separate town, now municipality
                346986,  # Novi Beograd - extended New Belgrade areas
                
                # Vračar District (Premium Residential Area)
                51647,   # Neimar - around St. Sava Temple
                51648,   # Vračar micro-location 
                51721,   # Vračar micro-location
                51765,   # Vračar micro-location
                51976,   # Krunski Venac
                52148, 52149, 52152, 52153, 52154, 52155, 52156, 52157,  # Vračar subdivisions
                52158, 52159, 52160, 52161, 52163, 52164, 52166, 52167,  # Vračar subdivisions  
                52168, 52169, 52170, 52171, 52174, 52175, 52176, 52177,  # Vračar subdivisions
                52178, 52179, 52180, 52182, 52184, 52185, 52186, 52187,  # Vračar subdivisions
                52188, 52190, 52191, 52192, 52193, 52195, 52196, 52205,  # Vračar subdivisions
                52240,   # Slavija square area
                52308,   # Čubura neighborhood
                52496, 52561, 52564,  # Additional Vračar micro-locations
                
                # Central Vračar & Surrounding Areas
                53031, 53037, 53057, 53060, 53128, 53133, 53430, 53482,  # Central areas
                53662,   # Englezovac/Savinac
                53699, 53743, 53761, 53769, 53777,  # Additional central micro-locations
                54075, 54134, 54191, 54308,  # Gradić Pejton area
                54310, 54527, 54585, 54645, 54651, 54677, 54738, 54814, 54859,  # Extended areas
                55007,   # Vračar center
                55238, 55298, 55354, 55365, 55383,  # Central residential areas
                55615, 55649, 55764, 55769, 55808, 55896,  # Crveni Krst area
                56091, 56243, 56306, 56348, 56357, 56358,  # Kalenić area
                56359, 56400, 56447,  # Additional central locations
                
                # New Belgrade (Novi Beograd) - Modern Residential Blocks
                56515,   # Blok 61-63 area
                56569, 56581, 56627, 56659,  # Additional New Belgrade areas
                56947,   # Blok 21-24 area  
                57114, 57245, 57320,  # Blok 45-50 area
                57340, 57490, 57803, 57817, 57841,  # Blok 65-67 area
                57876, 58067, 58244, 58274, 58352,  # Blok 70-72 area
                58447, 58528, 58713, 58768,  # Ušće area
                58822,   # Studentski Grad (Student City)
                58948, 58956, 59098, 59219, 59222, 59233, 59234,  # Extended NB areas
                59321, 59345, 59346, 59359, 59360, 59363, 59364,  # New Belgrade extensions
                
                # Extended Districts & Subdivisions  
                321814, 321844, 321874, 321904,  # District administrative codes
                345509, 345981, 345982, 345983, 345984, 345985, 345986,  # Extended district codes
                345987, 345988, 345989, 345990, 345991, 345992, 345994,  # Extended district codes
                346671, 346673, 346675, 346892, 346893, 346894, 347870,  # Additional districts
                
                # Specific Neighborhood Subdivisions
                525207,  # Specific subdivision code
                530949, 530950, 531079, 531122,  # Neighborhood subdivisions
                531257, 531258, 531259, 531542,  # Additional subdivisions
                534212, 534213, 534287, 534288, 534289, 534290,  # Voždovac subdivisions
                534416, 534465, 534466, 534467, 534468, 534470,  # Voždovac subdivisions
                534688,  # Banjica (Voždovac)
                534724,  # Autokomanda (Voždovac) 
                534760,  # Jajinci (Voždovac)
                534905,  # Braće Jerković (Voždovac)
                534906,  # Dušanovac (Voždovac)
                534908,  # Pašino Brdo (Voždovac)
                535035, 535036, 535105, 535106,  # Additional subdivisions
                535195, 535196, 535197, 535198, 535199, 535200,  # More subdivisions
                535201, 535202, 535203, 535483, 535484, 535485,  # More subdivisions  
                535589, 535590, 535591, 535592, 535716,  # Final subdivisions
                
                # Palilula & Eastern Belgrade Areas
                537326, 537327, 537328, 537329, 537330, 537331,  # Palilula subdivisions
                537332, 537333, 537334, 537335,  # Višnjica (Palilula)
                537336, 537337, 537339,  # Additional Palilula areas
                538000, 538001, 538002, 538003, 538004,  # Karaburma (Palilula)
                538005,  # Kotež (Palilula)
                538007, 538101, 538102, 538103, 538104,  # Ćalije (Palilula)
                538106,  # Rospi Ćuprija (Palilula)
                538107, 538174,  # Hadžipopovac (Palilula)
                538175, 538225, 538231,  # Profesorska Kolonija (Palilula)
                538232, 538276, 538277,  # Additional Palilula micro-locations
                538990, 538991, 538993, 538995,  # Viline Vode (Palilula)
                538998, 539000, 539001, 539004, 539005, 539006,  # Palilula extensions
                539009, 539010, 539011, 539012,  # Bogoslovija (Palilula)
                539017,  # Deponija area (Palilula)
                539021, 539022, 539023, 539024, 539025, 539026,  # Eastern micro-areas
                539027, 539028, 539034, 539035, 539036, 539037, 539044   # Final eastern areas
            ],
        },
    ],
    'FieldQueries': [],
    'FieldORQueries': [
        {
            'FieldName': 'CategoryIds',
            'FieldValues': [
                '1' if search_type == 'buy' else '13',  # 1=buy, 13=rent
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
    'CategoryId': '1' if search_type == 'buy' else '13',
    'SearchTypeIds': [
        1 if search_type == 'buy' else 2,  # 1=buy, 2=rent
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
    'BaseTaxonomy': '/nekretnine/prodaja-stanova' if search_type == 'buy' else '/nekretnine/izdavanje-stanova',
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

# URL to parse filter parameters (location codes)
# https://www.halooglasi.com/nekretnine/prodaja-stanova?grad_id_l-lokacija_id_l-mikrolokacija_id_l=40381%2C40574%2C40769%2C40772%2C40776%2C40783%2C40784%2C40787%2C40788%2C51647%2C51976%2C52240%2C52308%2C53662%2C54308%2C55007%2C55896%2C56358%2C56515%2C56947%2C57320%2C57841%2C58352%2C58768%2C58822%2C346980%2C346982%2C346983%2C346984%2C346985%2C346986%2C525616%2C527587%2C529392%2C534654%2C534688%2C534724%2C534760%2C534905%2C534906%2C534908%2C537335%2C538004%2C538005%2C538104%2C538106%2C538174%2C538231%2C538995%2C539012%2C539017&cena_d_from=110000&cena_d_to=126000&cena_d_unit=4&kvadratura_d_from=45&kvadratura_d_unit=1&broj_soba_order_i_from=4&broj_soba_order_i_to=9&sprat_order_i_from=3&dodatno_id_ls=12000004
# https://www.halooglasi.com/nekretnine/prodaja-stanova?grad_id_l-lokacija_id_l-mikrolokacija_id_l=40772%2C40776%2C40784%2C51647%2C51976%2C52240%2C52308%2C53662%2C54308%2C55007%2C55896%2C56358%2C56515%2C56947%2C57320%2C57841%2C58352%2C58768%2C58822%2C346980%2C346982%2C346983%2C346984%2C346985%2C346986%2C534688%2C534724%2C534760%2C534905%2C534906%2C534908%2C537335%2C538004%2C538005%2C538104%2C538106%2C538174%2C538231%2C538995%2C539012%2C539017%2C51648%2C51721%2C51765%2C52148%2C52149%2C52152%2C52153%2C52154%2C52155%2C52156%2C52157%2C52158%2C52159%2C52160%2C52161%2C52163%2C52164%2C52166%2C52167%2C52168%2C52169%2C52170%2C52171%2C52174%2C52175%2C52176%2C52177%2C52178%2C52179%2C52180%2C52182%2C52184%2C52185%2C52186%2C52187%2C52188%2C52190%2C52191%2C52192%2C52193%2C52195%2C52196%2C52205%2C52496%2C52561%2C52564%2C53031%2C53037%2C53057%2C53060%2C53128%2C53133%2C53430%2C53482%2C53699%2C53743%2C53761%2C53769%2C53777%2C54075%2C54134%2C54191%2C54310%2C54527%2C54585%2C54645%2C54651%2C54677%2C54738%2C54814%2C54859%2C55238%2C55298%2C55354%2C55365%2C55383%2C55615%2C55649%2C55764%2C55769%2C55808%2C56091%2C56243%2C56306%2C56348%2C56357%2C56359%2C56400%2C56447%2C56569%2C56581%2C56627%2C56659%2C57114%2C57245%2C57340%2C57490%2C57803%2C57817%2C57876%2C58067%2C58244%2C58274%2C58447%2C58528%2C58713%2C58948%2C58956%2C59098%2C59219%2C59222%2C59233%2C59234%2C59321%2C59345%2C59346%2C59359%2C59360%2C59363%2C59364%2C321814%2C321844%2C321874%2C321904%2C345509%2C345981%2C345982%2C345983%2C345984%2C345985%2C345986%2C345987%2C345988%2C345989%2C345990%2C345991%2C345992%2C345994%2C346671%2C346673%2C346675%2C346892%2C346893%2C346894%2C347870%2C525207%2C530949%2C530950%2C531079%2C531122%2C531257%2C531258%2C531259%2C531542%2C534212%2C534213%2C534287%2C534288%2C534289%2C534290%2C534416%2C534465%2C534466%2C534467%2C534468%2C534470%2C535035%2C535036%2C535105%2C535106%2C535195%2C535196%2C535197%2C535198%2C535199%2C535200%2C535201%2C535202%2C535203%2C535483%2C535484%2C535485%2C535589%2C535590%2C535591%2C535592%2C535716%2C537326%2C537327%2C537328%2C537329%2C537330%2C537331%2C537332%2C537333%2C537334%2C537336%2C537337%2C537339%2C538000%2C538001%2C538002%2C538003%2C538007%2C538101%2C538102%2C538103%2C538107%2C538175%2C538225%2C538232%2C538276%2C538277%2C538990%2C538991%2C538993%2C538998%2C539000%2C539001%2C539004%2C539005%2C539006%2C539009%2C539010%2C539011%2C539021%2C539022%2C539023%2C539024%2C539025%2C539026%2C539027%2C539028%2C539034%2C539035%2C539036%2C539037%2C539044&cena_d_from=110000&cena_d_to=126000&cena_d_unit=4&kvadratura_d_from=45&kvadratura_d_unit=1&broj_soba_order_i_from=4&broj_soba_order_i_to=9&sprat_order_i_from=3&dodatno_id_ls=12000004

# Telegram Bot Configuration
# These values are loaded from config.properties file or environment variables
# To get these values:
# 1. Create a bot with @BotFather on Telegram
# 2. Get the bot token from @BotFather  
# 3. Get your chat ID by messaging @userinfobot
# 4. Copy config.properties.template to config.properties and update values
TELEGRAM_BOT_TOKEN = config_loader.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = config_loader.get("TELEGRAM_CHAT_ID")
