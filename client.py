import socket


# send request on server
def request(req: str):
    # connection
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.103.25', 8888))
    print('!connected')
    # sending request
    client.send(req.encode('utf-8'))
    # getting answer
    data = client.recv(1024)
    print(f"Message: {data.decode('utf-8')}")
    # ending
    client.close()
