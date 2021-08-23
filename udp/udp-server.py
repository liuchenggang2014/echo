import socket

# HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
HOST = ''  # listening to any ip address 0.0.0.0/0
PORT = 6666        # Port to listen on (non-privileged ports are > 1023)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print("Listening on " + HOST + ":" + str(PORT))
    while True:
        data, client_address = s.recvfrom(4096)
        print("receive data from " + str(client_address) + repr(data))
        if not data:
            break
        s.sendto(data,client_address)