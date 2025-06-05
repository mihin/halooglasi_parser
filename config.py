import fake_user_agent

user = fake_user_agent.user_agent()

base_url = "https://www.halooglasi.com"

# Variables for filtering
# Cost in euros
price_from = None
price_to = '850'

# Apartment area
apartment_area_from = '40'
apartment_area_to = None

# Number of rooms. For some reason, it has to be multiplied by 2
# For example if you want 1.5 it should be '3'
number_of_rooms_from = '3'
number_of_rooms_to = None

# If you need the filter “Pets allowed” - uncomment 'dodatno_id_ls'

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
    # 'cookie': 'ASP.NET_SessionId=ta3nxveegc5pj322ud3amy5t; _gcl_au=1.1.94090009.1734454042; _hjSessionUser_615092=eyJpZCI6IjQwYWRiY2I0LTZmN2UtNWNhZS1hMWQ4LWM1OWJiYjEwYWEwZSIsImNyZWF0ZWQiOjE3MzQ0NTQwNDQxNTQsImV4aXN0aW5nIjp0cnVlfQ==; cookiePolicyConfirmation=true; _gid=GA1.2.3149787.1734954143; __gfp_64b=wwzVFkakvV2ghBm9CiRhgUUPx4k3myMQWZPO0tD6fE3.h7|1734454042|2|||8,2,32; _hjSession_615092=eyJpZCI6ImNmZjFlYzZjLWQ2M2UtNGVlNS04NjFlLTdmODViZThhZjMzYiIsImMiOjE3MzQ5NjE2Mzg2NTksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _gat=1; _dc_gtm_UA-4090358-9=1; _ga_TWCNL05EK4=GS1.1.1734961637.8.1.1734963251.17.0.0; _ga=GA1.1.581282287.1734454042; _ga_81XFKQEL79=GS1.2.1734961637.6.1.1734963251.24.0.0; _ga_TPG5HZ7P2L=GS1.2.1734961637.6.1.1734963251.24.0.0',
    'origin': 'https://www.halooglasi.com',
    'priority': 'u=1, i',
    'referer': 'https://www.halooglasi.com/nekretnine/izdavanje-stanova?grad_id_l-lokacija_id_l-mikrolokacija_id_l=40776%2C51898%2C51976%2C52308%2C53061%2C53662%2C54308%2C54331%2C54620%2C54793%2C55007%2C55403%2C55896%2C56051%2C56358%2C56360%2C56489%2C56515%2C56947%2C56951%2C57320%2C57405%2C57503%2C57841%2C57869%2C58352%2C58416%2C58768%2C58822%2C59098%2C321934%2C346532%2C346673%2C346980%2C346982%2C346983%2C346984%2C346985%2C346986%2C347239%2C347240%2C347241%2C347242%2C347244%2C347245%2C347246%2C347247%2C347248%2C347249%2C347250%2C347251%2C347252%2C534688%2C534802%2C534905%2C537335%2C538004%2C538005%2C538104%2C538105%2C538106%2C538172%2C538174%2C538231%2C538263%2C538995%2C538996%2C539003%2C539012%2C539017&cena_d_to=800&cena_d_unit=4&kvadratura_d_from=40&kvadratura_d_unit=1&broj_soba_order_i_from=3&namestenost_id_l=563%2C562&ostalo_id_ls=12100002%2C12100012&display=map',
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
    ],
    'MultiFieldORQueries': [
        {
            'FieldName': 'grad_id_l-lokacija_id_l-mikrolokacija_id_l',
            'FieldValues': [  # Numerical area codes
                40776,
                51898,
                51976,
                52308,
                53061,
                53662,
                54308,
                54331,
                54620,
                54793,
                55007,
                55403,
                55896,
                56051,
                56358,
                56360,
                56489,
                56515,
                56947,
                56951,
                57320,
                57405,
                57503,
                57841,
                57869,
                58352,
                58416,
                58768,
                58822,
                59098,
                321934,
                346532,
                346673,
                346980,
                346982,
                346983,
                346984,
                346985,
                346986,
                347239,
                347240,
                347241,
                347242,
                347244,
                347245,
                347246,
                347247,
                347248,
                347249,
                347250,
                347251,
                347252,
                534688,
                534802,
                534905,
                537335,
                538005,
                538104,
                538106,
                538172,
                538174,
                538231,
                538263,
                538995,
                538996,
                539003,
                539012,
                539017,
            ],
        },
    ],
    'FieldQueries': [],
    'FieldORQueries': [
        {
            'FieldName': 'CategoryIds',
            'FieldValues': [
                '13',
            ],
        },
        {
            'FieldName': 'namestenost_id_l',
            'FieldValues': [
                '564', # unfurnished
                '563',  # furnished, semi-furnished
                '562',
            ],
        },
        {   # Uncomment if the filter “Pets allowed” is needed
            # 'FieldName': 'dodatno_id_ls',
            # 'FieldValues': [
            #     '12000009',
            # ],
        },
        {
            'FieldName': 'ostalo_id_ls',
            'FieldValues': [
                '12100002',  # Air conditioner
                '12100012',  # Internet
            ],
        },
    ],
    'HasValueQueries': [],
    'GeoPolygonQuery': {},
    'GeoCircleQuery': {},
    'CategoryId': '13',
    'SearchTypeIds': [
        2,
        3,
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
    'BaseTaxonomy': '/nekretnine/izdavanje-stanova',
    'RenderSEOWidget': True,
}
