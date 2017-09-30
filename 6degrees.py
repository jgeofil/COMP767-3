import json, csv
import matplotlib.pyplot as plt
from random import choice, shuffle
import numpy as np
from scipy.stats import chi2_contingency as chi
from random import choice
from itertools import combinations_with_replacement

data = None

with open('jsons/all.json') as fp:
    data = json.load(fp)


ha = dict()

for p in data:
    ha[p['id']] = [x['id'] for x in p['dates']]

def rec(i, r, l, m):
    if r in l:
        return i
    if i > m:
        return -1
    for u in l:
        if u in ha:
            x = rec(i+1, r, ha[u], m)
            if x > 0:
                return x
    return -1

for _ in range(1000):
    if _%20 == 0:
        print(_)
    p1 = choice(data)['id']

    p2 = choice(data)['id']

    res = rec(0, p1, ha[p2], 6)
    if res != -1:
        print(res)


