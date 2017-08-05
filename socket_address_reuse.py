"""If you run a Python socket server on a specific port and try to rerun it after closing it once, you
won't be able to use the same port.The remedy to this problem is to enable the socket reuse option, SO_REUSEADDR ."""

import socket


def reuse_socket_addr():
    sock = socket.socket()
    # get the old state of the SO_REUSEADDR option
    old_state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print("Old sock state : {}".format(old_state))

    # enable SO_REUSEADDR option
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    new_state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
    print("New sock state : {}".format(new_state))

    local_port = 8282

    # create socket object srv for server
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind socket
    srv.bind(('', local_port))
    # make server listen for 1 incoming connection
    srv.listen(1)
    print("Listening on port : {}".format(local_port))

    while True:
        try:
            connection, addr = srv.accept()
            print(connection)
            print(addr)
            print('Connected by {}:{}'.format(addr[0], addr[1]))
        except KeyboardInterrupt:
            break
        except socket.error as msg:
            print(msg)


if __name__ == '__main__':
    reuse_socket_addr()
