import dns.resolver
import os
import json


def get_csv_domain_data():
    folder_path = str(os.path.abspath(__file__))[
        0:-len(os.path.basename(__file__))] + "data/"

    file_name = "test.csv"

    data = []

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(os.path.join(folder_path, file_name), mode='r') as file:
        for line in file:
            try:
                data.append(line.strip("\n")[0:-1])
            except StopIteration:
                continue

    return data[0:-1]


domain_names = get_csv_domain_data()
RRs = ['A', 'AAAA', 'NS', 'MX']
JSON_dump = {}

for name in domain_names:

    JSON_dump[name] = {}

    for record in RRs:
        JSON_dump[name][record] = {}
        answers = None

        try:
            answers = dns.resolver.query(name, record)
        except Exception as error:
            print('###')
            print(name, record, error)
            print('###')
            continue

        if record == 'A':

            JSON_dump[name][record]['IPv4'] = []

            for rdata in answers:
                JSON_dump[name][record]['IPv4'].append(str(rdata))

        if record == 'AAAA':

            JSON_dump[name][record]['IPv6'] = []

            for rdata in answers:
                JSON_dump[name][record]['IPv6'].append(str(rdata))

        elif record == 'NS':

            # rdata = str(answers.rrset).split(' ')
            JSON_dump[name][record]['names'] = []

            for data in answers.rrset:
                JSON_dump[name][record]['names'].append(str(data))

        elif record == 'MX':
            JSON_dump[name][record]['exchange'], JSON_dump[name][record]['preference'] = [
            ], []

            for rdata in answers:

                answer = (str(rdata).split(' '))

                try:
                    JSON_dump[name][record]['exchange'].append(answer[0])

                    JSON_dump[name][record]['preference'].append(answer[1])
                except Exception as error:
                    break

JSON_final = json.loads(json.dumps(JSON_dump, indent=4))

with open('./data/data.json', mode='w', encoding='utf-8') as json_file:
    json.dump(JSON_final, json_file, ensure_ascii=False, indent=4)
