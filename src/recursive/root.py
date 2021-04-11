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

load_dotenv()  # take environment variables from .env

DEBUG_MODE=str(os.environ['DEBUG'])

with open(str(os.environ['TOTAL_DATA']), mode='r') as file:
    data=json.load(file)

topLevelDomains=[]

for key in data:
    domain=key.split('.')[-1]
    if domain not in topLevelDomains:
        topLevelDomains.append(domain)

serv=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serv.bind((str(os.environ['HOSTNAME']),
           int(os.environ['ROOT_DOMAIN_PORT'])))

serv.listen(5)

while 1:
    conn, addr=serv.accept()

    # Great client
    conn.send(b"I am ROOT LEVEL DOMAIN")

    data=str(conn.recv(int(os.environ['BYTES_TO_RECEIVE'])))

    if not data:
        break

    # Bytes to DNSMessageCacheHandler Object
    ProtocolMessage: DNSMessageCacheHandler=DNSMessageCacheHandler(
        **json.loads(f"{eval(str(data)[1:])}"))

    '''
    At this point in the code, the original client that made
    the request for the domain name and all the related resources
    for it, does not actually know where the resources are
    This information is, instead of being given back to the client
    itself, is used by the root level domain server to make a
    request to a top level domain

    How does it know where the top level domain is? In the real world,
    the root level domain is a server that is connected to a distributed
    dataset of millions of registered top level domains

    Locally, here, it's just a different port number.

    Should the Root Server now send the entire DNS packet to the TLDs?
    It doesn't make sense to do that. What the Root is capable of is
    bookeeping `what` domains are available `where`. The `where` problem is
    solved. The `what` domains have been extracted above into the list
    `topLevelDomains`.

    The next logical step is to check if the request URL's domain
    is actually acknowledged and known by the Root

    The next `if` condition is exactly that
    '''

    if ProtocolMessage.GetStrForWebsiteDomain() in topLevelDomains:

        '''
        Great! We know where to hit a TLD to get back some data
        Ideally, the TLD provides the NS RRsets, and the ALDs provide
        the A, AAAA, and MX RRsets

        What should then the request to the TLD then be?
        It should a DNS query
        What question should it have?
        The complete domain name - the value of the hostname
        For example, `google.com`
        '''
        client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((str(os.environ['HOSTNAME']), int(
            os.environ['TOP_LEVEL_DOMAIN_PORT'])))

        '''
        Alright, so, it now makes sense to send the old DNSMessageCacheHandler, with the
        question field set to the domain name
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
    print('Local DNS disconnected')
