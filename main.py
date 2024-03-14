import socket
from db_helper import *

# creating server
server = socket.create_server(('192.168.0.100', 8888))

while True:
    # connection
    server.listen()
    print('!listen')
    client, address = server.accept()
    print('!client connected')
    # getting request
    client_data = client.recv(1024).decode('utf-8')
    print(f"Message: {client_data}")
    # sending result of registration
    if client_data.startswith('!r'):
        info = client_data.split(' ')[1].split('!')
        client.send(registration(*info).encode('utf-8'))
    # sending all user's data
    if client_data.startswith("!gai"):
        username = client_data.split(' ')[1]
        client.send(get_all_info(username).encode('utf-8'))
    # updating image
    if client_data.startswith("!ui"):
        username, img = client_data.split(' ')[1].split('!')
        client.send(update_image(username, img).encode('utf-8'))
