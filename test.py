
from numpy import random
from scipy.spatial import distance

def closest_node(node, nodes):
        closest_index = distance.cdist([node], nodes).argmin()
        return nodes[closest_index]

a = [[92,92],[378,796]]
some_pt = [1, 2]
print(a)
print(some_pt)
print(closest_node(some_pt, a))
