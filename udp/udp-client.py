import socket

HOST = '35.194.230.220'  # The server's hostname or IP address
PORT = 6666        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

    # Send data
    s.sendto(b'Hello, world', (HOST, PORT))

    # Receive response
    data, server = s.recvfrom(4096)
    print('Received', repr(data))

