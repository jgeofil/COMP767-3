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

print(data[0])
data = [x for x in data if 'Zodiac Sign' in x]

d = dict()
s = []
z = dict()

for p in data:
    d[p['id']] = p['Zodiac Sign']
    if p['Zodiac Sign'] not in s:
        s.append(p['Zodiac Sign'])
        z[p['Zodiac Sign']] = 1
    else:
        z[p['Zodiac Sign']] += 1


order = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

ind = [s.index(x) for x in order]

s = np.array(s)[ind]

ds = dict()
for i, sign in enumerate(s):
    ds[sign] = i

mat = np.zeros((len(s), len(s)))

total = 0

for p1 in data:
    for p2 in p1['dates']:
        if p2['id'] in d:
            total += 1
            i = ds[p1['Zodiac Sign']]
            j = ds[d[p2['id']]]
            mat[i, j] = mat[i, j] + 1
            mat[j, i] = mat[j, i] + 1

mat = np.array(mat)



print(z)


for i in range(len(s)):
    for j in range(len(s)):
        ma = np.array(list(mat))
        mat[i,j] = (ma[i,j]/total/2) / ((z[s[i]]/len(data)) * (z[s[j]]/len(data)))


fig, ax = plt.subplots()
print(mat)
img = plt.imshow(mat)
ax.set_yticks(range(12))
ax.set_yticklabels(s)
ax.set_xticklabels(['' for _ in range(12)])
fig.colorbar(img)
plt.show()