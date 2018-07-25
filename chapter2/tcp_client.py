import socket

target_host = '127.0.0.1'
target_port = 9090
target_data = 'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n'


# AF_INET parameter means the use of standard IPv4 address or hostname
# SOCK_STREAM means this is a TCP client
def tcp_client():
    # create socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect the client
    client.connect((target_host, target_port))
    # send some data
    client.send(target_data)
    # receive some data
    response = client.recv(4096)
    print response

if __name__ == '__main__':
    tcp_client()
