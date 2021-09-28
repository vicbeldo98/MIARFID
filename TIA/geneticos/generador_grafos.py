import string
import random
import json
edges = {}
idx = 0
for i in list(string.ascii_uppercase):
    for j in list(string.ascii_uppercase):
        if i != j:
            edges[idx] = [i, j, random.randint(1, 1000)]
            idx += 1

print(edges)
with open('edges.json', 'w') as f:
    json.dump(edges, f)
