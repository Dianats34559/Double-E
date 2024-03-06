import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.103.25', 8888))

while True:
    data = client.recv(1024)
    print(data.decode('utf-8'))

    client.send(input().encode('utf-8'))
