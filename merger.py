import json

concat = []

for file in ['a', 'bcd', 'efghi', 'jklmn', 'oz']:
    with open(file+'.json') as fp:
        concat = concat + json.load(fp)

with open('all.json', 'w+') as of:
    json.dump(concat, of)