#!/usr/bin/env python3

# Making a Raw HTTP Connection to Google Maps

import http.client
import json
from urllib.parse import quote_plus


def geocode(address):
    base = '/maps/api/geocode/json'
    path = '{}?address={}&sensor=false'.format(base, quote_plus(address))
    # print(path)
    connection = http.client.HTTPConnection('maps.google.com')
    connection.request('GET', path)
    # reply is bytes-string , so we need to deocde for converting it into
    # normal string
    raw_reply = connection.getresponse().read().decode()
    # Bprint(raw_reply)
    reply = json.loads(raw_reply)
    print(reply['results'][0]['geometry']['location'])


if __name__ == '__main__':
    address = '207 N. Defiance St, Archbold, OH'
    geocode(address)
