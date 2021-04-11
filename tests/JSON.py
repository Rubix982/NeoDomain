import json

with open('./data.json', mode='r') as file:
    data = json.load(file)

# topLevelDomains = []

for key in data:
    print(key)
#     domain = key.split('.')[-1]
#     if domain not in topLevelDomains:
#         topLevelDomains.append(domain) 

# print(topLevelDomains)