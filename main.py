import socket

server = socket.create_server(('192.168.103.25', 8888))

while True:
    server.listen()
    print('!listen')
    client, address = server.accept()
    print('!client connected')

    data = client.recv(1024)
    print(f"Message: {data.decode('utf-8')}")

    client.send(input().encode('utf-8'))



