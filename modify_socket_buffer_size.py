import socket

SEND_BUFFER_SIZE = 4096
RECIEVE_BUFFER_SIZE = 4096


def modify_buffer_size():
    sock = socket.socket()

    # Get size of socket's send buffer
    bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print('Buffer size [Before] : {}'.format(bufsize))

    # set new size of socket's buffer
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, SEND_BUFFER_SIZE)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, RECIEVE_BUFFER_SIZE)

    # get new socket's buffer size
    bufsize = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
    print('Buffer size [After] : {}'.format(bufsize))


if __name__ == '__main__':
    modify_buffer_size()
