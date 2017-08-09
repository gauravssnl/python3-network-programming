#!/usr/bin/env python3

# Send a big UDP datagram to learn the MTU of the network path.

try:
	import IN
except:
	import sys
	# change this path as required. I am using virtualenv
	sys.path.append('/usr/lib/python3.5/plat-x86_64-linux-gnu/'
)
	import IN
import socket

if not 	hasattr(IN, 'IP_MTU'):
	raise RuntimeError('cannot perfom MTU discovery on this combination of oS & Python distribution ')

def send_big_datagram(host, port):
	print(host, port)
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.IPPROTO_IP, IN.IP_MTU_DISCOVER, IN.IP_PMTUDISC_DO)
	sock.connect((host, port))
	try:
		sock.send(b'#' * 65000)
	except socket.error:
		print('Alas, the dtatagram did not make it')
		max_mtu = sock.getsockopt(socket.IPPROTO_IP, IN.IP_MTU)
		print('Actual MTU: {}'.format(max_mtu))
	else:
		print('The big datagram was sent!')


if __name__ == '__main__':
	import argparse
	parser= argparse.ArgumentParser(description='Send UDP packet to get MTU')
	parser.add_argument('host', help='host to which to target the packet')
	parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port(default 1060)')
	args = parser.parse_args()
	send_big_datagram(args.host, args.p)