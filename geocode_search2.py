#!/usr/bin/env python3

# Fetching a JSON Document from the Google Geocoding API

import requests


def geocode(address):
    parameters = {'address': address, 'sensor': 'false'}
    base = 'http://maps.googleapis.com/maps/api/geocode/json'
    response = requests.get(base, params=parameters)
    answer = response.json()
    print(answer['results'][0]['geometry']['location'])


if __name__ == '__main__':
    #address = '207 N. Defiance St, Archbold, OH'
    address = '15th cross, Maleshwaram,Banglore'
    geocode(address)
