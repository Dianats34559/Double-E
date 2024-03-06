import socket
from db_helper import registration

server = socket.create_server(('192.168.103.25', 8888))

while True:
    server.listen()
    print('!listen')
    client, address = server.accept()
    print('!client connected')

    client_data = client.recv(1024).decode('utf-8')
    print(f"Message: {client_data}")
    if client_data.startswith('!r'):
        info = client_data.split(' ')[1].split('!')
        print(info)
        client.send(registration(*info).encode('utf-8'))



