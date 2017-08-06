import os
import socket
import threading
import socketserver

# we need to define encode function for converting string to bytes string
# this will be use for sending/receiving data via socket
encode = lambda text: text.encode()

# we need to define deocde function for converting bytes string to string
# this will convert bytes string sent/recieved via socket to string
decode = lambda byte_text: byte_text.decode()

SERVER_HOST = 'localhost'
# tell kernel to pick port dynamically
SERVER_PORT = 0
BUFF_SIZE = 1024
ECHO_MSG = 'Hello echo server'


class ForkedClient():
    """ A client to test forking server"""

    def __init__(self, ip, port):
        # create a socket
        self.sock = socket.socket()
        # Connect to server
        self.sock.connect((ip, port))

    def run(self):
        """Client plays with the server"""
        # send data to server
        current_process_pid = os.getpid()
        print('PID {} Sending echo message to server : "{}"'.format(
            current_process_pid, ECHO_MSG))
        sent_data_length = self.sock.send(encode(ECHO_MSG))
        print('Sent {} characters so far...'.format(sent_data_length))

        # Display server response
        response = self.sock.recv(BUFF_SIZE)
        print('PID {} received: {}'.format(current_process_pid, decode(response[5:])))

    def shutdown(self):
        """	Cleanup client socket """
        self.sock.close()


class ForkingServerRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # send echo back to client
        data = self.request.recv(BUFF_SIZE)
        current_process_pid = os.getpid()
        response = '{0} : {1}'.format(current_process_pid, decode(data))
        print(
            'Server sending response [current_process_id: data] = [{}]'.format(response))
        self.request.send(encode(response))
        return


class ForkingServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    """ Nothing to add here. Inherited everything necessary from parents """
    pass


def main():
    # Launch the server
    server = ForkingServer((SERVER_HOST, SERVER_PORT),
                           ForkingServerRequestHandler)
    ip, port = server.server_address  # retreive the port number
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.setDaemon(True)  # do nt hang on exit
    server_thread.start()
    print('Server loop running PID: {}'.format(os.getpid()))

    # Launch the client(s)
    client1 = ForkedClient(ip, port)
    client1.run()

    client2 = ForkedClient(ip, port)
    client2.run()

    # clean up
    server.shutdown()
    client1.shutdown()
    client2.shutdown()
    server.socket.close()


if __name__ == '__main__':
    main()
