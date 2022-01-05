import argparse
import json
from collections import defaultdict, namedtuple
'''
User must input the pathway to the json file

'''
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path",
                    type=str, required=True,
                    help="Enter the path")

args = parser.parse_args()

file_path = args.path
with open(file_path, 'r') as f:
    data = json.loads(f.read())

'''
Need to give a score to all 23 terms directly under HP:0000118
1 Find all keys that have have HP:0000118 as a parent:
2 Store the indices 23 of them
3 Go through the dictionary again find all HP with any of the indices and add +1 everytime they appear
4 Compare the final score between the 23 indices and print them in order from from highest to lowest
'''

# BFS
# Going two depth into the tree
d = {}
# root of graph we are focusing on
root = '0000118'
# iterate all nodes in graph
for node in data:
    # take children of 118
    children = data[node]['ParentId'] 
    # check if node is child of 118
    if root in children:
        # iterate all child nodes of child of 118
        for node_child in data:
            # take parents of the child of child of 118
            node_children = data[node_child]['ParentId']
            # if first child is the parent of the second child of 118, add 1
            if node in node_children:
                d[node] = d.get(node, 0) + 1
print(d)
    
# Printing in order of highest to lowest
answer = sorted(d, key=d.get, reverse=True)
print('\n')
print('Final answer:', '\n')
print(answer)
