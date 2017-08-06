import os
import socket
import threading
import socketserver

# we need to define encode function for converting string to bytes string
# this will be used for sending/receiving data via socket
encode = lambda text: text.encode()

# we need to define deocde function for converting bytes string to string
# this will convert bytes string sent/recieved via socket to string
decode = lambda byte_text: byte_text.decode()

SERVER_HOST = 'localhost'
# tell kernel to pick port dynamically
SERVER_PORT = 0
BUFF_SIZE = 1024
ECHO_MSG = 'Hello echo server'


def client(ip, port, message):
    """ A client to test threading mmixin socket server """
    # connect to server
    sock = socket.socket()
    sock.connect((ip, port))
    try:
        sock.sendall(encode(message))
        response = sock.recv(BUFF_SIZE)
        print('Client received : {}'.format(decode(response)))
    finally:
        sock.close()


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """ An example of threaded TCP request handler """

    def handle(self):
        data = self.request.recv(BUFF_SIZE)
        current_thread = threading.current_thread()
        response = '{} : {}'.format(current_thread.name, decode(data))
        self.request.sendall(encode(response))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """ Nothing to add here, inherited everything from parents """
    pass


def main():
    # run server
    server = ThreadedTCPServer(
        (SERVER_HOST, SERVER_PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address  # get ip addreess
    # start a thread with the server --one thread per request
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print('Serever loop running on thread {}'.format(server_thread.name))

    # Run clients
    client(ip, port, "Hello from client1")
    client(ip, port, "Hello from client2")
    client(ip, port, "Hello from client3")
    # server cleanup
    server.shutdown()


if __name__ == '__main__':
    main()
