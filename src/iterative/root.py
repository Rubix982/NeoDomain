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
sys.path.insert(1, os.path.abspath('.') + str(os.environ['MODEL_PATH']))

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

serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serv.bind((str(os.environ['HOSTNAME']),
           int(os.environ['ROOT_DOMAIN_PORT'])))

while 1:
    data, addr = serv.recvfrom(int(os.environ['BYTES_TO_RECEIVE']))

    if not data:
        break

    # Bytes to DNSMessageCacheHandler Object
    ProtocolMessage: DNSMessageCacheHandler = DNSMessageCacheHandler(
        **json.loads(f"{eval(str(data)[1:])}"))

    if ProtocolMessage.GetStrForWebsiteDomain() in topLevelDomains:
        ProtocolMessage.answers = str(os.environ['TOP_LEVEL_DOMAIN_PORT'])
        serv.sendto(ProtocolMessage.EncodeObject(), addr)
    else:
        if DEBUG_MODE == 'ON':
            print(ProtocolMessage.GetStrForWebsiteDomain(), topLevelDomains)
        serv.sendto(b"[ROOT_LEVEL_DOMAIN] 400: Bad request", addr)
    print('Local DNS disconnected')
