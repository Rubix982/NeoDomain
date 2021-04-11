import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('0.0.0.0', 4043))
client.send(b"I am Local DNS Server<br>")
print(str(client.recv(4096)))
client.close()
