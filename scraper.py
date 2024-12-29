import requests
import json


def fetch_data(url, cookies, headers, json_data, output_file="halooglasi_data.json"):
    response = requests.post(url, cookies=cookies, headers=headers, json=json_data)

    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code}")

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(response.json(), file, ensure_ascii=False, indent=4)

    return response.json()
