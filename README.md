# Scraper for https://www.halooglasi.com/
This application allows you to get information about apartments from https://www.halooglasi.com/ and find an apartment in Belgrade.

## Installation

Cloning a repository:

```git clone https://github.com/shestakovitch/halooglasi_parser.git```

Creating a virtual environment:

```python3 -m venv venv```


Activating the virtual environment:

```source venv/bin/activate```

Installing the required packages from requirements.txt﻿:

```pip3 install -r requirements.txt```

## Description

1. In "config.py," you can see many filters. For example, price_to, apartment_area_from, number_of_rooms_from etc. 

2. By default, my app's area is around the city center. To change it, you should change 'MultiFieldORQueries'['FieldValues'] in json_data in config.py.

3. By default, this app saves data to output_file="halooglasi_data.xlsx" on your computer. If you want to save it on your Google Drive:

You should install gspread. Here is a link to the documentation: https://docs.gspread.org/

Also, you should enable API Access for a Project: https://docs.gspread.org/en/v6.1.3/oauth2.html#enable-api-access

You will automatically download a JSON file with credentials. It may look like this:

{

    "type": "service_account",
    
    "project_id": "api-project-XXX",
    
    "private_key_id": "2cd … ba4",
    
    "private_key": "-----BEGIN PRIVATE KEY-----\nNrDyLw … jINQh/9\n-----END PRIVATE KEY-----\n",
    
    "client_email": "473000000000-yoursisdifferent@developer.gserviceaccount.com",
    
    "client_id": "473 … hd.apps.googleusercontent.com",
    
    ...
}

Save it as "creds.json" in the root folder of the project.

Then you should create a new sheet on your Google Drive, name it "cityexpert_parsing_report" and share it with "client_email" from "creds.json".
