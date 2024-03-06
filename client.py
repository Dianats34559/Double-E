import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.103.25', 8888))

print('!connected')

while True:
    client.send(input().encode('utf-8'))

    data = client.recv(1024)
    print(f"Message: {data.decode('utf-8')}")


