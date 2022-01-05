'''
The HPO continues to be updated on a regular basis. Focusing on the subsection of
the DAG which is rooted in the top-level "Phenotypic abnormality"
'''
import requests
from collections import defaultdict, namedtuple
import argparse

text = requests.get('https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo').text

indices = []
for i, line in enumerate(text.split('\n')):
    if line == '[Term]':
        indices.append(i)
indices.append(-1)

# parent -> child
graph_parent_child = defaultdict(list)
graph_child_parent = defaultdict(list)
definition = {}
text_split = text.split('\n')
# build graph relation
# start and end indices for each node
for i, j in zip(indices, indices[1:]):
    # selecting every single line that is a list for a phenotype
    data = text_split[i:j]
    for line in data:
        if line.startswith('id'):
            # This returns a list and you split -> element of list
            id = line.split()[1].split(':')[1]

        elif line.startswith('is_a'):
            num = line.split()[1].split(':')[1]
            graph_parent_child[num].append(id)
            # This is parent child relationship
            graph_child_parent[id].append(num)
        elif line.startswith('name'):
            definition[id] = line[len('name: '):]

# find all nodes related to 0000118
# DFS
# parent child -> element is the children
q = ['0000118']
print(q)

# This takes '0000118' as an unique element no two elements can repeat
visited = set(['0000118'])
while q:
    n = q.pop()
    # value q to the list, and pops first index and adding it as [n]
    q += graph_parent_child[n]
    visited.add(n)

# remove nodes in child - parent graph that is not related to 0000118, child to parent takes consideration of everything
for node in list(graph_child_parent):
    if node not in visited:
        del graph_child_parent[node]

# create JSON response object in nested dictionary format
for node in graph_child_parent:
    graph_child_parent[node] = {
        'Id': node,
        'ParentId': graph_child_parent[node],
        'Description': definition[node]
    }

#print(graph_parent_child['0000118'])
# print(graph_parent_child['0000119'])

import json
import argparse
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output',
                    type=str, required=False,
                    help='Output File Name.', default= ''
                    )

args = parser.parse_args()


current_datetime = datetime.datetime.now().strftime("%Y-%m-%d")
str_current_datetime = str(current_datetime)
print(str_current_datetime)


if args.output == '':
  # Default name should hpo_<datetime>.json  
  # Do not put a -o if there is no input
  file_name = "hpo_{}.json".format(datetime.datetime.now().strftime("%Y-%m-%d"))
else:
  file_name = args.output

with open(file_name, 'w') as f:
    json.dump(graph_child_parent, f, indent =4)



