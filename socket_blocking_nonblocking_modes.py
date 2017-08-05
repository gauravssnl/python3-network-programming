"""By default, TCP sockets are placed in a blocking mode. This means the control is not returned
to your program until some specific operation is complete. For example, if you call the
connect() API, the connection blocks your program until the operation is complete.So,we need to set socket mode to non-blocking"""

import socket


def set_socket_mode():
    s = socket.socket()
    # set socket to blocking mode by passing 1 as argument .For non-blocking
    # mode pass 0 as argument
    s.setblocking(1)
    # set timeout
    s.settimeout(0.5)
    # bind socket to localhost
    s.bind(('127.0.0.1', 0))

    socket_address = s.getsockname()
    print('Server  launched on socket : {}'.format(socket_address))

if __name__ == '__main__':
    set_socket_mode()
