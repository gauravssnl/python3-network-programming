import socket

host = 'localhost'

# we need to define encode function for converting string to bytes string
#  this will be use for sending/receiving data via socket
encode = lambda text: text.encode()

# we need to define deocde function for converting bytes string to string
# this will convert bytes string sent/recieved via socket to string

decode = lambda byte_text: byte_text.decode()


def echo_client(port, message="Hello"):
    # create a TCP socket
    sock = socket.socket()
    server_address = (host, port)
    # connect to server
    print("Connecting to server ")
    sock.connect(server_address)

    # send data
    try:
        # send message
        print("Sending data: {}".format(message))
        # sendall need bytes string ,so we need to use encode  to convert plain
        # string to bytes string
        sock.sendall(encode(message))
        # Look for response
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print("Recieved from server: {}".format(decode(data)))
    except socket.error as e:
        print("socket error: {}".format(e))
    except Exception as e:
        print("other exception: {}".format(e))
    finally:
        print("Closing connection to server")
        sock.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Simple TCP echo client')
    parser.add_argument("--port", action="store",
                        dest="port", type=int, required=True)
    parser.add_argument("--message", action="store",
                        dest="message", required=False)
    get_args = parser.parse_args()
    port = get_args.port
    message = get_args.message
    if message:
        echo_client(port, message)
    else:
        echo_client(port)
