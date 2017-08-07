import asyncore
import socket

LOCAL_SERVER_HOST = 'localhost'
REMOTE_SERVER_HOST = 'www.google.com'
BUFFSIZE = 2048


class PortForwarder(asyncore.dispatcher):
    def __init__(self, ip, port, remoteip, remoteport, backlog=5):
        asyncore.dispatcher.__init__(self)
        self.remoteip = remoteip
        self.remoteport = remoteport
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip, port))
        self.listen(backlog)

    def handle_accept(self):
        conn, addr = self.accept()
        print('Connected to: {}'.format(addr))
        Sender(Receiver(conn), self.remoteip, self.remoteport)


class Receiver(asyncore.dispatcher):
    def __init__(self, conn):
        asyncore.dispatcher.__init__(self, conn)
        self.from_remote_buffer = b''
        self.to_remote_buffer = b''
        self.sender = None

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(BUFFSIZE)
        print('\nReceiver read: {}'.format(read))
        self.from_remote_buffer += read

    def writable(self):
        return (len(self.to_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
        print('\nReceiver write: {}'.format(self.to_remote_buffer[:sent]))
        self.to_remote_buffer = self.to_remote_buffer[sent:]

    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()


class Sender(asyncore.dispatcher):
    def __init__(self, receiver, remoteaddr, remoteport):
        asyncore.dispatcher.__init__(self)
        self.receiver = receiver
        receiver.sender = self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((remoteaddr, remoteport))

    def handle_connect(self):
        pass

    def handle_read(self):
        read = self.recv(BUFFSIZE)
        print('\nSender read: {}'.format(read))
        self.receiver.to_remote_buffer += read

    def writable(self):
        return(len(self.receiver.from_remote_buffer) > 0)

    def handle_write(self):
        sent = self.send(self.receiver.from_remote_buffer)
        print('\nSender write: {}'.format(
            self.receiver.from_remote_buffer[:sent]))
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[
            sent:]

    def handle_close(self):
        self.close()
        self.receiver.close()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Port forwarding example')
    parser.add_argument('--local-host', action='store',
                        dest='local_host', default=LOCAL_SERVER_HOST)
    parser.add_argument('--local-port', action='store',
                        dest='local_port', type=int, required=True)
    parser.add_argument('--remote-host', action='store',
                        dest='remote_host', default=REMOTE_SERVER_HOST)
    parser.add_argument('--rmote-port', action='store',
                        dest='remote_port', type=int, default=80)
    given_args = parser.parse_args()
    local_host, remote_host = given_args.local_host, given_args.remote_host
    local_port, remote_port = given_args.local_port, given_args.remote_port
    print('Starting port forwarding local {}:{} => {}:{}'.format(
        local_host, local_port, remote_host, remote_port))
    PortForwarder(local_host, local_port, remote_host, remote_port)
    asyncore.loop()
