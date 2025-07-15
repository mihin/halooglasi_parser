import requests
import json
import os


def fetch_data(url, cookies, headers, json_data, output_file=None):
    if output_file is None:
        # Get the project root directory (three levels up from this file)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        data_dir = os.path.join(project_root, "data")
        os.makedirs(data_dir, exist_ok=True)
        output_file = os.path.join(data_dir, "halooglasi_data.json")
    response = requests.post(url, cookies=cookies, headers=headers, json=json_data)

    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code}")

    response_data = response.json()
    
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(response_data, file, ensure_ascii=False, indent=4)

    # Return the Ads data directly for processing
    return response_data.get("Ads", [])
