""" Simple Network Time Protocol Client(SNTP)
 Epoch & Unix Timestamp Conversion Tools https://www.epochconverter.com/ """
import socket
import struct
import time

NTP_SERVER = '0.uk.pool.ntp.org'
# epoch time :January 1,1970
TIME1970 = 2208988800


def sntp_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = b'\x1b' + 47 * b'\0'
    client.sendto(data, (NTP_SERVER, 123))
    data, address = client.recvfrom(1024)
    if data:
        print('Recieved data from : {}'.format(address))
        t = struct.unpack('!12I', data)[10]
        t -= TIME1970
        print('\tTime = {}'.format(time.ctime(t)))


if __name__ == '__main__':
    sntp_client()
