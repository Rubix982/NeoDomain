import socket
import json
import sys
import os
from DNSMessageCacheHandler import DNSMessageCacheHandler
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# CONFIGURATIONS
HOSTNAME = str(os.environ['HOSTNAME'])
ROOT_DOMAIN_PORT = int(os.environ['ROOT_DOMAIN_PORT'])
TOP_LEVEL_DOMAIN_PORT = int(os.environ['TOP_LEVEL_DOMAIN_PORT'])
AUTHORITATIVE_DOMAIN_PORT = int(os.environ['AUTHORITATIVE_DOMAIN_PORT'])
BYTES_TO_RECEIVE = int(os.environ['BYTES_TO_RECEIVE'])
IDENTIFICATION_COUNTER = str(os.environ['IDENTIFICATION_COUNTER'])

while True:
    websiteURL = str(input("Enter website hostname: "))

    websiteDomain = websiteURL.split('.')[-1]
    websiteHostname = '.'.join(websiteURL.split('.')[0:-1])

    # with open("cache.json", mode='r') as file:
    #     file.keys == domainNameToFind:

    # if data == None:
    #     print("Info does not exist in cache")
    # else:

    # Creating a new client with IPv4/TCP settings
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # -----------------------------------
    # Connect to Root Level Domain

    # # Connection command
    client.connect((HOSTNAME, ROOT_DOMAIN_PORT))

    # # Construct object to send

    ProtocolMessage: DNSMessageCacheHandler = DNSMessageCacheHandler()
    ProtocolMessage.setWebsiteConfig(websiteHostname, websiteDomain)
    ProtocolMessage.DefaultInit()

    # # Message to send
    client.send(ProtocolMessage.EncodeObject())

    # # Indicates the information received
    response = str(client.recv(BYTES_TO_RECEIVE))

    if '400' in response:
        print(response)
        sys.exit(1)

    # # # Convert to dict
    ProtocolMessage = DNSMessageCacheHandler(
        **json.loads(f"{eval(response[1:])}"))

    # # Closing client connection with server
    client.close()

    # -----------------------------------

    # -----------------------------------
    # Connect to Top Level

    # Creating a new client with IPv4/TCP settings
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # # Connection command
    client.connect((HOSTNAME, int(ProtocolMessage.__dict__['answers'])))

    # # Constructing package to send

    # # Message to send
    client.send(ProtocolMessage.EncodeObject())

    # # Indicates the information received
    response = str(client.recv(BYTES_TO_RECEIVE))

    if '400' in response:
        print(response)
        sys.exit(1)

    # # # Convert to dict
    ProtocolMessage = DNSMessageCacheHandler(
        **json.loads(f"{eval(response[1:])}"))

    # # Closing client connection with server
    client.close()

    # -----------------------------------

    # -----------------------------------
    # Connect to Authoritative Domain

    # Creating a new client with IPv4/TCP settings
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # # Connection command
    client.connect((HOSTNAME, int(ProtocolMessage.__dict__['answers'])))

    # # Message to send
    client.send(ProtocolMessage.EncodeObject())

    # # Indicates the information received
    response = str(client.recv(BYTES_TO_RECEIVE))

    if '400' in response:
        print(response)
        sys.exit(1)

    # # # Convert to dict
    ProtocolMessage = DNSMessageCacheHandler(
        **json.loads(f"{eval(response[1:])}"))

    # # Closing client connection with server
    client.close()

    # -----------------------------------

    print(ProtocolMessage.__dict__)

    ProtocolMessage.DumpToCache('./cache.json')
