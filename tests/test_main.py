import pytest
import requests
import requests_mock
from requests.exceptions import RequestException
from src.main import get_outages, get_site_info, filter_and_prepare_outages, post_site_outages

def test_get_outages(requests_mock):
    url = "https://api.krakenflex.systems/interview-tests-mock-api/v1/outages"
    outages_data = [{"id": "1", "begin": "2022-01-01T00:00:00.000Z", "end": "2022-01-02T00:00:00.000Z"}]
    requests_mock.get(url, json=outages_data)
    
    outages = get_outages()
    assert outages == outages_data

def test_get_site_info(requests_mock):
    site_id = "norwich-pear-tree"
    url = f"https://api.krakenflex.systems/interview-tests-mock-api/v1/site-info/{site_id}"
    site_info_data = {"id": site_id, "name": "Norwich Pear Tree", "devices": [{"id": "1", "name": "Device 1"}]}
    requests_mock.get(url, json=site_info_data)
    
    site_info = get_site_info(site_id)
    assert site_info == site_info_data

def test_filter_and_prepare_outages():
    outages = [
        {"id": "1", "begin": "2022-01-01T00:00:00.000Z", "end": "2022-01-02T00:00:00.000Z"},
        {"id": "2", "begin": "2021-12-31T23:59:59.000Z", "end": "2022-01-01T01:00:00.000Z"}
    ]
    site_info = {"id": "norwich-pear-tree", "name": "Norwich Pear Tree", "devices": [{"id": "1", "name": "Device 1"}]}
    filtered_outages = filter_and_prepare_outages(outages, site_info)
    
    assert filtered_outages == [{"id": "1", "name": "Device 1", "begin": "2022-01-01T00:00:00.000Z", "end": "2022-01-02T00:00:00.000Z"}]

def test_post_site_outages(requests_mock):
    site_id = "norwich-pear-tree"
    url = f"https://api.krakenflex.systems/interview-tests-mock-api/v1/site-outages/{site_id}"
    outages_data = [{"id": "1", "name": "Device 1", "begin": "2022-01-01T00:00:00.000Z", "end": "2022-01-02T00:00:00.000Z"}]
    requests_mock.post(url, json={"status": "success"})
    
    result = post_site_outages(site_id, outages_data)
    assert result == {"status": "success"}
