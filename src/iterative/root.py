# pylint: disable=no-member
import os
import sys
import json
import socket
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env

# Unable to find a way to do relative imports
# Resorting to prepanding the PYTHON PATH ENV
# with the path where the module exists
sys.path.insert(1, str(os.environ['MODEL_PATH']))

from DNSMessageCacheHandler import DNSMessageCacheHandler
# pylint: enable=no-member

DEBUG_MODE = str(os.environ['DEBUG'])

with open(str(os.environ['TOTAL_DATA']), mode='r') as file:
    data = json.load(file)

topLevelDomains = []

for key in data:
    domain = key.split('.')[-1]
    if domain not in topLevelDomains:
        topLevelDomains.append(domain)

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind((str(os.environ['HOSTNAME']),
           int(os.environ['ROOT_DOMAIN_PORT'])))

serv.listen(5)

while 1:
    conn, addr = serv.accept()
    data = str(conn.recv(int(os.environ['BYTES_TO_RECEIVE'])))

    if not data:
        break

    # Bytes to DNSMessageCacheHandler Object
    ProtocolMessage: DNSMessageCacheHandler = DNSMessageCacheHandler(
        **json.loads(f"{eval(str(data)[1:])}"))

    if ProtocolMessage.GetStrForWebsiteDomain() in topLevelDomains:
        ProtocolMessage.answers = str(os.environ['TOP_LEVEL_DOMAIN_PORT'])
        conn.send(ProtocolMessage.EncodeObject())
    else:
        if DEBUG_MODE == 'ON':
            print(ProtocolMessage.GetStrForWebsiteDomain(), topLevelDomains)
        conn.send(b"[ROOT_LEVEL_DOMAIN] 400: Bad request")
    conn.close()
    print('Local DNS disconnected')
