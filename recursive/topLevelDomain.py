import socket
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', 4044))
serv.listen(5)
while True:
    conn, addr = serv.accept()
    data = str(conn.recv(4096))
    if not data:
        break
    conn.send(b"I am TOP LEVEL DOMAIN<br>")
    print(data)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('0.0.0.0', 4045))
    client.send(b"I am TOP LEVEL DOMAIN<br>")
    print(str(client.recv(4096)))    

    conn.close()
    print('ROOT LEVEL DOMAIN disconnected')
