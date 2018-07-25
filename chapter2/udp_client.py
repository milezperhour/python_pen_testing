import socket

target_host = '127.0.0.1'
target_port = 9000
target_data = 'AAAAAAAAA'

def udp_client():
    # create socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # send some data
    client.sendto(target_data, (target_host, target_port))
    # receive some data
    data, addr = client.recvfrom(4096)
    print data, addr

if __name__ == '__main__':
    udp_client()
