import json

data = []
with open('./jsons/all.temp.json', 'r') as fp:
    data = json.load(fp)
with open('./jsons/all.json', 'w+') as fp:
    json.dump(data, fp, indent=2)