#!/usr/bin/env python3
# Find the WWW service of an arbitrary host using getaddrinfo()

import socket
import sys


def connect_to(host_or_ip):
    try:
        infolist = socket.getaddrinfo(
            host_or_ip, 'www', 0, socket.SOCK_STREAM, 0, socket.AI_ADDRCONFIG | socket.AI_V4MAPPED)
    except socket.gaierror as e:
        print('Name service failure:', e.args[1])
        sys.exit(1)

    info = infolist[0]
    sock_args = info[0:3]
    address = info[4]
    s = socket.socket(*sock_args)
    try:
        s.connect(address)
    except socket.error as e:
        print('Network failure:', e.args[1])
    else:
        print('Sucess: host', info[3], 'is listening on port 80')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Connect host/ip over port 80')
    parser.add_argument('hostname', help='hostname that you want to connect')
    args = parser.parse_args()
    hostname = args.hostname
    connect_to(hostname)
