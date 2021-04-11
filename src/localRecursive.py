import socket
import json
import sys
import os
from models.DNSMessageCacheHandler import DNSMessageCacheHandler
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# CONFIGURATIONS
HOSTNAME = str(os.environ['HOSTNAME'])
ROOT_DOMAIN_PORT = int(os.environ['ROOT_DOMAIN_PORT'])
BYTES_TO_RECEIVE = int(os.environ['BYTES_TO_RECEIVE'])
CACHE_FILE_LOCATION = str(os.environ['CACHE_FILE'])

while True:

    # Get the input for the website URL
    websiteURL = str(input("Enter website hostname: "))

    # Split it for the host and the domain
    websiteHostname = '.'.join(websiteURL.split('.')[0:-1])
    websiteDomain = websiteURL.split('.')[-1]

    # Check mark for the existence of data within the cache
    cacheFound = False

    with open(CACHE_FILE_LOCATION, mode='r') as file:
        JSONdata = json.load(file)

    # Checking if the data is in cache
    for key in JSONdata:
        if key == websiteURL:
            # This data exists in the cache
            print(f"From cache,\n\"{JSONdata[key]}\"\n")
            cacheFound = True

    # If the requested domain exists
    # in the cache, proceed to the next query
    if cacheFound:
        continue

    # This control flow indicates that the data is
    # not in the cache

    # Creating a new client with IPv4/TCP setting
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

    if '400: Bad request' in response:
        print(response)
        sys.exit(1)

    # # # Convert to dict
    ProtocolMessage = DNSMessageCacheHandler(
        **json.loads(f"{eval(response[1:])}"))

    # # Closing client connection with server
    client.close()

    # -----------------------------------

    print(ProtocolMessage.__dict__)

    ProtocolMessage.DumpToCache(CACHE_FILE_LOCATION)
