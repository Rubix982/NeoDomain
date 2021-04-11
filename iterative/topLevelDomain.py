import socket
import json
import os

from dotenv import load_dotenv
from DNSMessageCacheHandler import DNSMessageCacheHandler

load_dotenv()  # take environment variables from .env.

DEBUG_MODE = str(os.environ['DEBUG'])

with open('../scripts/data/data.json', mode='r') as file:
    JSONdata = json.load(file)

hostNames = []

for key in JSONdata:
    hostName = '.'.join(key.split('.')[0:-1])
    if hostName not in hostNames:
        hostNames.append(hostName)

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((str(os.environ['HOSTNAME']),
           int(os.environ['TOP_LEVEL_DOMAIN_PORT'])))

serv.listen(5)

while True:
    conn, addr = serv.accept()
    data = str(conn.recv(int(os.environ['BYTES_TO_RECEIVE'])))
    if not data:
        break

    # Bytes to DNSMessageCacheHandler Object
    ProtocolMessage: DNSMessageCacheHandler = DNSMessageCacheHandler(
        **json.loads(f"{eval(str(data)[1:])}"))

    if ProtocolMessage.GetStrForWebsiteHost() in hostNames:
        ProtocolMessage.answers = str(os.environ['AUTHORITATIVE_DOMAIN_PORT'])

        if 'names' in JSONdata[ProtocolMessage.GetStrForWebsite(
        )]['NS']:
            ProtocolMessage.authority = JSONdata[ProtocolMessage.GetStrForWebsite(
            )]['NS']['names']
        conn.send(ProtocolMessage.EncodeObject())
    else:
        if DEBUG_MODE == 'ON':
            print(
                f"\"{ProtocolMessage.GetStrForWebsite()}\", \"{ProtocolMessage.GetStrForWebsiteHost()}\", \"{hostNames}\"")
        conn.send(b"[TOP_LEVEL_DOMAIN] 400: Bad request")
    conn.close()
    print('Local DNS disconnected')
