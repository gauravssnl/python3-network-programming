#!/usr/bin/env python3

# Talking to Google Maps Through a Bare Socket

import socket
from urllib.parse import quote_plus

raw_text = """GET /maps/api/geocode/json?address={}&sensor=false HTTP/1.1\r\nHost: maps.google.com:80\r\nUser-Agent: Python-3\r\nConnection: close\r\n\r\n"""


def geocode(address):
    sock = socket.socket()
    host = 'maps.google.com'
    port = 80
    sock.connect((host, port))
    request = raw_text.format(quote_plus(address))
    sock.sendall(request.encode('ascii'))
    raw_reply = b''
    while True:
        more = sock.recv(4096)
        if not more:
            break
        raw_reply += more
    print(raw_reply.decode('utf-8'))


if __name__ == '__main__':
    address = '207 N. Defiance St, Archbold, OH'
    geocode(address)
