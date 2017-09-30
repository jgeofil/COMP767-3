import json, csv
import matplotlib.pyplot as plt
from random import choice, shuffle
import numpy as np

data = None

with open('jsons/all.json') as fp:
    data = json.load(fp)

shuffle(data)
data = data

ages = [int(x['Age'].split()[0]) if 'Age' in x and x['Age'].split()[0].isdigit() else 0 for x in data]
number = [len(x['dates']) for x in data]

ups = [sum([y['up'] for y in x['dates']])/(len(x['dates']) or 1) for x in data]
downs = [-sum([y['down'] for y in x['dates']])/(len(x['dates']) or 1) for x in data]

plt.scatter(number, ups, s=1, alpha=0.5)
plt.scatter(number, downs, s=1, alpha=0.5)
plt.ylim((-1000,1500))
plt.xlim((0,60))
plt.xlabel("Total number of relationships")
plt.ylabel("Downvotes (Orange) Upvotes (Blue)")
plt.show()