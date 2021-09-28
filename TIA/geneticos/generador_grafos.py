import string
import random
import json
edges = {}
idx = 0
for i in list(string.ascii_uppercase):
    for j in list(string.ascii_uppercase):
        #   for k in list(string.ascii_uppercase):
        if i != j:
            edges[idx] = [i, j, random.randint(1, 1000)]
            idx += 1
for i in range(len(edges.keys())):
    if random.randint(0, 5) > 3:
        del edges[i]
        idx -= 1
idx += 1
with open(str(idx) + '_edges.json', 'w') as f:
    json.dump(edges, f)
