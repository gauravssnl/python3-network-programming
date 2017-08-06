import sys
import socket
import argparse


# we need to define encode function for converting string to bytes string
# this will be used for sending/receiving data via socket
encode = lambda text: text.encode()

# we need to define deocde function for converting bytes string to string
# this will convert bytes string sent/recieved via socket to string
decode = lambda byte_text: byte_text.decode()


def main():
    # set up argument parsing
    parser = argparse.ArgumentParser(description='socket error examples')
    parser.add_argument('--host', action='store', dest='host', required=False)
    parser.add_argument('--port', action='store',
                        dest='port', type=int, required=False)
    parser.add_argument('--file', action='store', dest='file', required=False)
    given_args = parser.parse_args()
    host = given_args.host
    port = given_args.port
    filename = given_args.file

    # First try-except block --create socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print("Error in creating socket: {}".format(e))
        sys.exit(1)

    # Second try-except bock --connect to given host with given port
    try:
        s.connect((host, port))
    except socket.gaierror as e:
        print("Address-related error connecting to server: {}".format(e))
        sys.exit(1)
    except socket.error as e:
        print("Connection error: {}".format(e))
        sys.exit(1)

    # Third try-except block -- sending data
    try:
        # function need bytes string as argument not plain string
        s.sendall(encode("GET {} HTTP/1.0\r\n\r\n".format(filename)))
    except socket.error as e:
        print("Error in sending data: {}".format(e))
        sys.exit(1)

    while True:
        # Fourth try-ecept block --waiting for receiving data from remote host
        try:
            buf = s.recv(2048)
        except socket.error as e:
            print("Error in receiving data: {}".format(e))
        if not len(buf):
            break
        # write the data
        # conver bytes string to string
        sys.stdout.write(decode(buf))
        sys.stdout.write('\n')


if __name__ == '__main__':
    main()
