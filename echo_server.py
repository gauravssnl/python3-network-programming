import socket

host = 'localhost'
data_payload = 2048
backlog = 5

# we need to define encode function for converting string to bytes string
# this will be use for sending/receiving data via socket
encode = lambda text: text.encode()

# we need to define deocde function for converting bytes string to string
# this will convert bytes string sent/recieved via socket to string
decode = lambda byte_text: byte_text.decode()


def echo_server(port):
    # create a TCP socket
    sock = socket.socket()
    # enable reuse address/port
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # bind socket to port
    server_address = (host, port)
    print("Starting up echo server on %s port %s" % server_address)
    sock.bind(server_address)
    # Listen to clients,backlog argument specifies the maximum number of
    # queued connections
    sock.listen(backlog)

    while True:
        print("Waiting to receive message from client")
        client, addr = sock.accept()
        print("Connected client :{}".format(addr))
        data = client.recv(data_payload)
        if data:
            # decode is used to convert bytes string to string
            data = decode(data)
            print("Data Received from client : {}".format(data))
            # encode is used to convert string to bytes string
            # required by send function
            client.send(encode(data))
            print("Data sent back to client : {}".format(data))
        # end connection
        client.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Socket echo Server Example')
    parser.add_argument("--port", action="store",
                        dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)
