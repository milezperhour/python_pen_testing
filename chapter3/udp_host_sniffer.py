# simply run this script in one terminal
# open another terminal and enter: ping google.com

import socket
import os

# host to listen on
HOST = '192.168.1.100'

def sniffing(host, win, socket_protocol):
    while 1:
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        sniffer.bind((host, 0))

        # a socket option that includes the IP headers in our captured packets
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        # if we're using Windows, we need to send IOCTL to the network card driver to enable promiscuous mode
        if win == 1:
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        # read in a single raw packet in binary form
        # receives all IP headers along with any high protocols such as TCP, UDP, or ICMP
        print sniffer.recvfrom(65565)

# create a raw socket and bind it to the public interface
def main(host):
    if os.name == 'nt':
        sniffing(host, 1, socket.IPPROTO_IP)
    else:
        sniffing(host, 0, socket.IPPROTO_ICMP)

if __name__ == '__main__':
    main(HOST)
