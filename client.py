import socket


def request(req: str):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.103.25', 8888))

    print('!connected')

    client.send(req.encode('utf-8'))

    data = client.recv(1024)
    print(f"Message: {data.decode('utf-8')}")

    client.close()


