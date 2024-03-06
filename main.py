import socket
from db_helper import registration

# creating server
server = socket.create_server(('192.168.0.25', 8888))

while True:
    # connection
    server.listen()
    print('!listen')
    client, address = server.accept()
    print('!client connected')
    # getting request
    client_data = client.recv(1024).decode('utf-8')
    print(f"Message: {client_data}")
    # sending answer
    if client_data.startswith('!r'):
        info = client_data.split(' ')[1].split('!')
        client.send(registration(*info).encode('utf-8'))
