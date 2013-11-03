#!/usr/bin/python

# graph.py 
# Graph algorithms for TSP Art 
# 
# Author: Tommy Tracy II 
# Created: 11/2/2013
#

from math import *

def full_graph(nodes):
	edges = []
	while(len(nodes) != 0):
		current_node = nodes.pop(0)
		current_y = current_node[0]
		current_x = current_node[1]

		for i in range(len(nodes)):
			temp = nodes[i]
			temp_y = temp[0]
			temp_x = temp[1]
			
			edges.append((current_node, temp, hypot(current_x - temp_x, current_y - temp_y)))
	return edges 
