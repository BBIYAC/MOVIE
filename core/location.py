import requests
import os
import json
from pathlib import Path

class Location(object):
    def __init__(self, LOCATION_API_KEY):
        self.LOCATION_API_KEY = LOCATION_API_KEY
        # https://velog.io/@yvvyoon/python-current-location-coordinate

    def get_location(self):
        url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={self.LOCATION_API_KEY}'
        data = {
            'considerIp': True,
        }

        result = requests.post(url, data).text
        location = json.loads(result)
        location = location['location']

        return location

    def get_location_api(self):
        BASE_DIR = Path(__file__).resolve().parent.parent
        secret_file = os.path.join(BASE_DIR, 'secrets.json')

        with open(secret_file) as f:
            secrets = json.loads(f.read())
            LOCATION_API_KEY = secrets.get("LOCATION_API_KEY")

        return LOCATION_API_KEY

    def get_place_location(self, place):
        # https://maps.googleapis.com/maps/api/geocode/json?address='신도림'&key=AIzaSyDCxLJSmZTFfFABCiyX0i9rFx73dZ01nq0
        address = str(place)
        key = str(self.get_location_api())
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address, key)
        headers = {'content-type': 'application/json'}
        response = requests.post(url, headers=headers)
        response = response.text
        response = json.loads(response)
        results = response.get('results')
        geometry = results[0]['geometry']
        location = geometry.get('location')
        return location