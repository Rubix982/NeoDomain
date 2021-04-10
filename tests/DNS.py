import dns.resolver

answers = dns.resolver.query('google.com', 'AAAA')
# print(str(answers.rrset.name), str(answers.rrset.ttl), str(
#     answers.rrset.covers), str(answers.rrset.rdclass), str(answers.rrset.rdtype))
# print(str(answers.rrset))
# for data in answers.rrset:
#     print(data)
# for rdata in answers:
#     print(rdata.rrset
print(answers.rrset)
