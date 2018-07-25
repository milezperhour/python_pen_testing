import socket
import threading

bind_ip = '0.0.0.0'
bind_port = 9090


print '[*] Listening on %s:%d' % (bind_ip, bind_port)

# this is the client-handling thread
def handle_client(client_socket):
    # print out what the client sends
    request = client_socket.recv(1024)
    print '[*] Received: ' + request
    # send back a packet
    client_socket.send('ACK!')
    client_socket.close()

def tcp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    print '[*] Listening on %s:%d' % (bind_ip, bind_port)

    while 1:
        client, addr = server.accept()
        print '[*] Accepted connection from: %s:%d' %(addr[0], addr[1])
        # spin up the client thread to handle incoming data
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == '__main__':
    tcp_server()

