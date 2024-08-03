import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.krakenflex.systems/interview-tests-mock-api/v1'

def save_to_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_outages():
    url = f"{BASE_URL}/outages"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    outages = response.json()
    save_to_file(outages, 'files/outages.json')
    return outages

def get_site_info(site_id):
    url = f"{BASE_URL}/site-info/{site_id}"
    headers = {"x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    site_info = response.json()
    save_to_file(site_info, 'files/site_info.json')
    return site_info

def post_site_outages(site_id, outages):
    url = f"{BASE_URL}/site-outages/{site_id}"
    headers = {"x-api-key": API_KEY, "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(outages))
    response.raise_for_status()
    result = response.json()
    save_to_file(result, 'files/post_result.json')
    return result

def filter_and_prepare_outages(outages, site_info):
    filtered_outages = []
    for outage in outages:
        if datetime.fromisoformat(outage['begin'][:-1]) < datetime(2022, 1, 1):
            for device in site_info['devices']:
                if outage['id'] == device['id']:
                    filtered_outages.append({
                        "id": outage['id'],
                        "name": device['name'],
                        "begin": outage['begin'],
                        "end": outage['end']
                    })
    save_to_file(filtered_outages, 'files/filtered_outages.json')
    return filtered_outages

def main():
    try:
        outages = get_outages()
        site_info = get_site_info('norwich-pear-tree')
        filtered_outages = filter_and_prepare_outages(outages, site_info)
        post_site_outages('norwich-pear-tree', filtered_outages)
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
