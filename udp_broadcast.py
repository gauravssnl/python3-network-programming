# 1/usr/bin/env python3
# UDP client and server for broadcast messages on a local LAN

import socket

BUFFSIZE = 65535


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print("listening for datagrams at {}".format(sock.getsockname()))
    while True:
        data, address = sock.recvfrom(BUFFSIZE)
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))


def client(network, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    text = 'Broadcast Datagram!'
    sock.sendto(text.encode('ascii'), (network, port))


if __name__ == '__main__':
    import argparse
    choices = {'server': server, 'client': client}
    parser = argparse.ArgumentParser(description='Send/Receive UDP broadcast')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument(
        'host', help='interface the server listens at, network the client connects to')
    parser.add_argument('-p', metavar='PORT', type=int,
                        default=1060, help='UDP port(default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
