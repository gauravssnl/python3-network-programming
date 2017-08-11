# 1/usr/bin/env python3
# Sending data over a stream but delimited as length-prefixed blocks

import socket
import struct

header_struct = struct.Struct('!I')  # message upto 2 ^ 32 -1 in length


def recvall(sock, length):
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError('Socket closed with {} bytes left', length)
        length -= len(block)
        blocks.append(block)
    return b''.join(blocks)


def get_blocks(sock):
    data = recvall(sock, header_struct.size)
    (block_length, ) = header_struct.unpack(data)
    return recvall(sock, block_length)


def put_blocks(sock, message):
    block_length = len(message)
    sock.send(header_struct.pack(block_length))
    sock.send(message)


def server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)
    print('Run this script in another window with -c option to connect')
    print('Listening at', sock.getsockname())
    sc, sockname = sock.accept()
    print('Accepted connection from', sockname)
    sock.shutdown(socket.SHUT_WR)
    while True:
        block = get_blocks(sc)
        if not block:
            break
        print('Block says:', repr(block))
    sc.close()
    sock.close()


def client(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.shutdown(socket.SHUT_RD)
    put_blocks(sock, b'Beautiful is better than ugly.')
    put_blocks(sock, b'Explicit is better than implicit')
    put_blocks(sock, b'Simple is better than complex')
    put_blocks(sock, b'')
    sock.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Transmit and Receive blocks over TCP')
    parser.add_argument('hostname', nargs='?', default='127.0.0.1',
                        help='IP address or hostname (default: %(default)s)')
    parser.add_argument('-c', action='store_true', help='run as client')
    parser.add_argument('-p', type=int, metavar='port', default=1060,
                        help='TCP port number (default: %(default)s')
    args = parser.parse_args()
    function = client if args.c else server
    function((args.hostname, args.p))
