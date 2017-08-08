#!/usr/bin/env python3

#Turning a Hostname into an IP Address

import socket

host = 'wwww.python.org'
addr = socket.gethostbyname(host)
print('The IP address of {} is {}'.format(host, addr))
