import socket
import select

SERVER_HOST = 'localhost'
EOL1 = b'\n\n'
EOL2 = b'\n\r\n'

SERVER_RESPONSE = b"""HTTP/1.1 200 OK\r\nDate: Sunday, 6 August 2017
01:01:01 GMT\r\nContent-Type: text/plain\r\nContent-Length: 31\r\n\r\n
Hello from Epoll Server"""


class EpollServer:
    """ A socket server using epoll"""

    def __init__(self, host=SERVER_HOST, port=0):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host, port))
        self.sock.listen(1)
        # set socket to non-blocking mode
        self.sock.setblocking(0)
        # set socket as unbuffered
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        print("Started epoll server")
        self.epoll = select.epoll()
        # register our server's file descriptor for event notifications
        self.epoll.register(self.sock.fileno(), select.EPOLLIN)

    def run(self):
        """ execute epoll server operation """
        try:
            connections = {}
            requests = {}
            responses = {}
            while True:
                events = self.epoll.poll(1)
                for fileno, event in events:
                    if fileno == self.sock.fileno():
                        connection, address = self.sock.accept()
                        connection.setblocking(0)
                        self.epoll.register(
                            connection.fileno(), select.EPOLLIN)
                        connections[connection.fileno()] = connection
                        requests[connection.fileno()] = b''
                        responses[connection.fileno()] = SERVER_RESPONSE
                    elif event & select.EPOLLIN:
                        requests[fileno] += connections[fileno].recv(1024)
                        if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                            self.epoll.modify(fileno, select.EPOLLOUT)
                            # decode converts byte string to string
                            print('-' * 40 + '\n' +
                                  requests[fileno].decode()[:-2])
                    elif event & select.EPOLLOUT:
                        byteswritten = connections[
                            fileno].send(responses[fileno])
                        responses[fileno] = responses[fileno][byteswritten:]
                        if len(responses[fileno]) == 0:
                            self.epoll.modify(fileno, 0)
                            connections[fileno].shutdown(socket.SHUT_RDWR)
                    elif event & select.EPOLLHUP:
                        self.epoll.unregister(fileno)
                        connections[fileno].close()
                        del connections[fileno]
        finally:
            self.epoll.unregister(self.sock.fileno())
            self.epoll.close()
            self.sock.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Socket Server example with epoll')
    parser.add_argument('--port', action='store',
                        dest='port', type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    server = EpollServer(host=SERVER_HOST, port=port)
    server.run()
