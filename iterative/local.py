import socket

# CONFIGURATIONS
HOSTNAME = 'localhost'
ROOT_DOMAIN_PORT = 4043
TOP_LEVEL_DOMAIN_PORT = 4044
AUTHORITATIVE_DOMAIN_PORT = 4045
BYTES_TO_RECEIVE = 4096

# domainNameToFind = str(input("Enter domain name: "))

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

# # Message to send
client.send(b"I am Local DNS Server")

# # Indicats the information received
print(str(client.recv(BYTES_TO_RECEIVE)))

# # Closing client connection with server
client.close()

# -----------------------------------

# -----------------------------------
# Connect to Top Level

# Creating a new client with IPv4/TCP settings
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connection command
client.connect((HOSTNAME, TOP_LEVEL_DOMAIN_PORT))

# # Message to send
client.send(b"I am Local DNS Server")

# # Indicates the information received
print(str(client.recv(BYTES_TO_RECEIVE)))

# # Closing client connection with server
client.close()

# -----------------------------------

# -----------------------------------
# Connect to Authoritative Domain

# Creating a new client with IPv4/TCP settings
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connection command
client.connect((HOSTNAME, AUTHORITATIVE_DOMAIN_PORT))

# # Message to send
client.send(b"I am Local DNS Server")

# # Indicates the information received
print(str(client.recv(BYTES_TO_RECEIVE)))

# # Closing client connection with server
client.close()

# -----------------------------------
