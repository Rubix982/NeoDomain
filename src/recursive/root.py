# pylint: disable=no-member
import os
import sys
import json
import socket

# Unable to find a way to do relative imports
# Resorting to prepanding the PYTHON PATH ENV
# with the path where the module exists
sys.path.insert(1, '/home/saif/Desktop/DNS/src/models')

from DNSMessageCacheHandler import DNSMessageCacheHandler
from dotenv import load_dotenv
# pylint: enable=no-member

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('0.0.0.0', 4043))
serv.listen(5)
while True:
    conn, addr = serv.accept()
    data = str(conn.recv(4096))
    if not data:
        break
    conn.send(b"I am ROOT LEVEL DOMAIN<br>")
    print(data)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('0.0.0.0', 4044))
    client.send(b"I am ROOT LEVEL DOMAIN<br>")
    print(str(client.recv(4096)))    

    conn.close()
    print('Local DNS disconnected')
