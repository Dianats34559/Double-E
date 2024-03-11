import socket


# send request on server
def request(req: str):
    # connection
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with open('Data/server_ip', 'r') as ip:
        client.connect((ip.readline(), 8888))
        print('!connected')
        # sending request
        client.send(req.encode('utf-8'))
        # getting answer
        data = client.recv(1024)
        answer = data.decode('utf-8')
        print(f"Message: {answer}")
    # ending
    client.close()
    return answer
