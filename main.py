import socket

server = socket.create_server(('192.168.103.25', 8888))

while True:
    server.listen()
    print('listen...')
    print('')
    client, address = server.accept()
    print('client connected')
    print('')
    data = client.recv(1024).decode('utf-8')
    print(data)
    client.send("you are welcome".encode('utf-8'))
    print('Well done!')
