# pylint: disable=no-member
import os
import sys
import json
import socket

# Unable to find a way to do relative imports
# Resorting to prepanding the PYTHON PATH ENV
# with the path where the module exists
sys.path.insert(1, str(os.environ['MODEL_PATH'])

from DNSMessageCacheHandler import DNSMessageCacheHandler
from dotenv import load_dotenv
# pylint: enable=no-member

load_dotenv()  # take environment variables from .env.

DEBUG_MODE=str(os.environ['DEBUG'])

with open(str(os.environ['TOTAL_DATA']), mode='r') as file:
    JSONdata=json.load(file)

hostNames=[]

for key in JSONdata:
    hostName='.'.join(key.split('.')[0:-1])
    if hostName not in hostNames:
        hostNames.append(hostName)

serv=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind((str(os.environ['HOSTNAME']),
           int(os.environ['TOP_LEVEL_DOMAIN_PORT'])))

serv.listen(5)

while 1:
    conn, addr=serv.accept()

    # Great client
    conn.send(b"I am TOP LEVEL DOMAIN")

    data=str(conn.recv(int(os.environ['BYTES_TO_RECEIVE'])))

    if not data:
        break

    # Bytes to DNSMessageCacheHandler Object
    ProtocolMessage: DNSMessageCacheHandler=DNSMessageCacheHandler(
        **json.loads(f"{eval(str(data)[1:])}"))

    '''
    So basically, the Root says to the TLD, "yo bro, you got this hostname?
    I think I heard you knew about hostnames with these domain"

    And the TLD is basically, "yeah sure, bro, let me take a look into my list of
    hostnames, and I'll let ya know if something doesn't seem right"

    And the Root all the while is waiting for a response from the TLD like
    a very patient guy.

    Good peeps.
    '''
    if ProtocolMessage.GetStrForWebsiteHost() in hostNames:

        '''
        Now, we have this ProtocolMessage that contains the question - which
        the `hostname.domain` we are searching, and with the above `if` condition
        we could deduce that the required host does actually exist in some record
        in this TLD server - thus we can put whatever that data is into our
        `answers` field, and move onto finally sending this packet to the ALD
        so we can fetch our A, AAAA, and the MX records

        The step of adding the NS records is done in the next step with the
        `if` condition
        '''

        if 'names' in JSONdata[ProtocolMessage.GetStrForWebsite()]['NS']:
            ProtocolMessage.answers=JSONdata[ProtocolMessage.GetStrForWebsite(
            )]['NS']['names']

        '''
        Establishing a connection with the ALD as a client
        '''
        client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((str(os.environ['HOSTNAME']), int(
            os.environ['AUTHORITATIVE_DOMAIN_PORT'])))

        '''
        Now we send the ProtocolMessage packet to the ALD
        '''
        client.send(ProtocolMessage.EncodeObject())

        # # Indicates the information received
        response=str(client.recv(BYTES_TO_RECEIVE))

        if '400' in response:
            print(response)
            sys.exit(1)

        # # # Convert to dict
        ProtocolMessage=DNSMessageCacheHandler(
            **json.loads(f"{eval(response[1:])}"))
        conn.send(ProtocolMessage.EncodeObject())
    else:
        if DEBUG_MODE == 'ON':
            print(
                f"\"{ProtocolMessage.GetStrForWebsite()}\", \"{ProtocolMessage.GetStrForWebsiteHost()}\", \"{topLevelDomains}\"")
        conn.send(b"[ROOT_LEVEL_DOMAIN] 400: Bad request")
    conn.close()
    print('ROOT LEVEL DOMAIN disconnected')
