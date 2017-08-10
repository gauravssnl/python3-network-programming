#!/usr/bin/env python3
""" Modern Address Resolution """

import socket
import pprint


def get_address(host, port):
    print('Host: {} Port:{}'.format(host, port))
    infolist = socket.getaddrinfo(host, port)
    pprint.pprint(infolist)
    info = infolist[0]
    pprint.pprint(info[0:3])
    s = socket.socket(*info[0:3])
    pprint.pprint(info[4])
    s.connect(info[4])
    pprint.pprint('Connected to {}:{}'.format(info[4][0], info[4][1]))


if __name__ == '__main__':
    host = 'google.com'
    port = 'www'  # port = 80
    get_address(host, port)
