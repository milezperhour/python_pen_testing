import socket

bind_ip = '0.0.0.0'
bind_port = 9000

def udp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((bind_ip, bind_port))
    print 'Waiting on port: ' + str(bind_port)

    while 1:
        data, addr = server.recvfrom(1024)
        print data

if __name__ == '__main__':
    udp_server()

