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

DEBUG_MODE=str(os.environ['DEBUG'])

with open(str(os.environ['TOTAL_DATA']), mode='r') as file:
    JSONdata=json.load(file)

hostNames=[]

for key in JSONdata:
    hostName='.'.join(key.split('.')[0:-1])
    if hostName not in hostNames:
        hostNames.append(hostName)

serv=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind((str(os.environ['HOSTNAME']), int(
    os.environ['AUTHORITATIVE_DOMAIN_PORT'])))

serv.listen(5)

while 1:
    conn, addr=serv.accept()
    data=str(conn.recv(int(os.environ['BYTES_TO_RECEIVE'])))

    if not data:
        break

    # Bytes to DNSMessageCacheHandler Object
    ProtocolMessage: DNSMessageCacheHandler=DNSMessageCacheHandler(
        **json.loads(f"{eval(str(data)[1:])}"))

    print('-----')
    print('In Authoritative - when received')
    print(ProtocolMessage.__dict__)

    if ProtocolMessage.GetStrForWebsiteHost() in hostNames:
        ProtocolMessage.additional=[]

        # An A record will always exists
        ProtocolMessage.additional.append(JSONdata[ProtocolMessage.GetStrForWebsite(
        )]['A']['IPv4'])

        # If an IPv6 record exists in the data, append it
        if 'IPv6' in JSONdata[ProtocolMessage.GetStrForWebsite()]['AAAA']:

            ProtocolMessage.additional.append(JSONdata[ProtocolMessage.GetStrForWebsite(
            )]['AAAA']['IPv6'])

        # If a 'preference' MX record exists in the data, append it
        if 'preference' in JSONdata[ProtocolMessage.GetStrForWebsite()]['MX']:

            ProtocolMessage.additional.append(JSONdata[ProtocolMessage.GetStrForWebsite(
            )]['MX']['preference'])

        print('-----')
        print('In Authoritative - before sending')
        print(ProtocolMessage.__dict__)

        conn.send(ProtocolMessage.EncodeObject())
    else:
        if DEBUG_MODE == 'ON':
            print('----\nIn Debug!')            
            print(
                f"\"{ProtocolMessage.GetStrForWebsite()}\", \"{ProtocolMessage.GetStrForWebsiteHost()}\", \"{hostNames}\"")
        conn.send(b"[AUTHORITATIVE_LEVEL_DOMAIN] 400: Bad request")
    conn.close()
    print('TOP LEVEL DOMAIN disconnected')
