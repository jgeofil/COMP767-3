import json, csv
import matplotlib.pyplot as plt
from random import choice, shuffle

data = None

with open('all.json') as fp:
    data = json.load(fp)

shuffle(data)
data = data[:10000]

print(json.dumps(data[:10], indent=2, sort_keys=True))

ages = [int(x['Age'].split()[0]) if 'Age' in x and x['Age'].split()[0].isdigit() else 0 for x in data]
number = [len(x['dates']) for x in data]

rels = []
sexs = []

def there(a,b):
    for r in rels:
        if a in r and b in r:
            return True
    return False

for ac in data:
    np = [pa['id'] for pa in ac['dates'] if not there(pa, ac)]
    if len(sexs)%1000:
        print(len(sexs))
    if len(np) > 0:
        rels.append([ac['id'], 'dated'] + np)
    sexs.append([ac['id'], ac['Sexuality'] if 'Sexuality' in ac else 'U',
                 ac['Zodiac Sign'] if 'Zodiac Sign' in ac else 'U',
                 ac['Religion'] if 'Religion' in ac else 'U',
                 ac['Occupation'] if 'Occupation' in ac else 'U',
                 ac['Nationality'] if 'Nationality' in ac else 'U',
                 ac['Hair color'] if 'Hair color' in ac else 'U',
                 ac['Ethnicity'] if 'Ethnicity' in ac else 'U',
                 int(ac['Age'].split()[0] if ac['Age'].split()[0].isdigit() else 0) if 'Age' in ac else 'U',
                ])

with open('rels10.sif', 'w+') as f:
    spamwriter = csv.writer(f, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for r in rels:
        spamwriter.writerow(r)

with open('info10.tsv', 'w+') as f:
    spamwriter = csv.writer(f, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for r in sexs:
        spamwriter.writerow(r)



