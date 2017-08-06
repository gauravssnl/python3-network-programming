import select
import socket
import sys
import signal
import pickle
import struct


# we need to define encode function for converting string to bytes string
# this will be used for sending/receiving data via socket
encode = lambda text: text.encode()

# we need to define deocde function for converting bytes string to string
# this will convert bytes string sent/recieved via socket to string
decode = lambda byte_text: byte_text.decode()

SERVER_HOST = 'localhost'
CHAT_SERVER_NAME = 'server'

# some utilities


def send(channel, *args):
    buffer = pickle.dumps(args)
    value = socket.htonl(len(buffer))
    size = struct.pack("L", value)
    # buffer and size are already bytes string
    channel.send(size)
    channel.send(buffer)


def receive(channel):
    size = struct.calcsize("L")
    size = channel.recv(size)
    # print('n Test size {} whose length :{}'.format(size , len(size)))
    try:
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error as e:
        # print(e)
        return ''
    buf = ''
    while len(buf) < size:
        buf = channel.recv(size - len(buf))
    return pickle.loads(buf)[0]


class ChatServer:
    """ An example chat server using select """

    def __init__(self, port, backlog=5):
        self.clients = 0
        self.clientmap = {}
        self.outputs = []  # list output sockets
        self.server = socket.socket()
        # enable reusing socket adress
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        print('Server listening on port {}'.format(port))
        self.server.listen(backlog)
        # catch keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)

    def sighandler(self, signum, frame):
        """ Cleanup client outputs """
        # close the server """
        print('Shutting down server')
        # close existing client sockets
        for output in self.outputs:
            output.close()
        self.server.close()

    def get_client_name(self, client):
        """ Return name of client """
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '{}@{}'.format(name, host)

    def run(self):
        inputs = [self.server, sys.stdin]
        self.outputs = []
        running = True
        while running:
            try:
                readable, writeable, exceptional = select.select(
                    inputs, self.outputs, [])
            except select.error as e:
                break
            for sock in readable:
                if sock == self.server:
                    # handle server socket
                    client, address = self.server.accept()
                    print('Chat server: got connection {} from {}'.format(
                        client.fileno(), address))
                    # read the login name
                    cname = receive(client).split('NAME: ')[1]
                    # compute client name and send back
                    self.clients += 1
                    send(client, 'CLIENT: {}'.format(address[0]))
                    inputs.append(client)
                    self.clientmap[client] = (address, cname)
                    # send joining information to other clients
                    msg = '\nConnected: New Client {} from {}'.format(
                        self.clients, self.get_client_name(client))
                    for output in self.outputs:
                        send(output, msg)
                    self.outputs.append(client)

                elif sock == sys.stdin:
                    # handle standatrd input
                    junk = sys.stdin.readline()
                    running = False
                else:
                    # handle all other sockets
                    try:
                        data = receive(sock)
                        if data:
                            # send as new client's message
                            msg = '\n#[{}]>>{}'.format(
                                self.get_client_name(sock), data)
                            # send data to all except ourself
                            for output in self.outputs:
                                if output != sock:
                                    send(output, msg)
                        else:
                            print('Chat server {} hung up '.format(sock.fileno()))
                            self.clients -= 1
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)
                            # sending client leaving info to others
                            msg = '\n(Now hung up: Client from {})'.format(
                                self.get_client_name(sock))
                            for output in self.outputs:
                                send(output, msg)
                    except socket.error as e:
                        # Remove
                        inputs.remove(sock)
                        self.outputs.remove(sock)
        self.sever.close()


class ChatClient:
    """ A command line chat client using select"""

    def __init__(self, name, port, host=SERVER_HOST):
        self.name = name
        self.connected = False
        self.host = host
        self.port = port
        # Initial prompt
        self.prompt = '[{}]>'.format(
            '@'.join((name, socket.gethostname().split('.')[0])))
        # connect to server at port
        try:
            self.sock = socket.socket()
            self.sock.connect((host, port))
            print("now connected to chat server at port {}".format(port))
            self.connected = True
            # send my name
            send(self.sock, 'NAME: {}'.format(self.name))
            data = receive(self.sock)
            # contains client addresss, set it
            addr = data.split('CLIENT: ')[1]
            self.prompt = '[{}]>'.format(self.name, addr)
        except socket.error as e:
            print('Failed to connect to chats server at port {}'.format(self.port))
            sys.exit(1)

    def run(self):
        """ Chat client main loop """
        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()
                # wait for input from stdin and socket
                readable, writeable, exceptional = select.select(
                    [0, self.sock], [], [])
                for sock in readable:
                    if sock == 0:
                        data = sys.stdin.readline().strip()
                        if data:
                            send(self.sock, data)
                    elif sock == self.sock:
                        data = receive(self.sock)
                        if not data:
                            print('Client shutting down')
                            self.connected = False
                            break
                        else:
                            sys.stdout.write('{}\n'.format(data))
                            sys.stdout.flush()
            except KeyboardInterrupt:
                print('Client interrupted.')
                self.sock.close()
                break


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Socket server with select')
    parser.add_argument('--name', action='store', dest='name', required=True)
    parser.add_argument('--port', action='store',
                        dest='port', type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    name = given_args.name

    if name == CHAT_SERVER_NAME:
        server = ChatServer(port)
        server.run()
    else:
        client = ChatClient(name=name, port=port)
        client.run()
