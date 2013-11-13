#!/usr/bin/python

# graph.py 
# Graph algorithms for TSP Art 
# 
# Author: Tommy Tracy II 
# Created: 11/2/2013
#

from math import *
from scipy.spatial import Delaunay
import numpy as np

# Returns the edges in the Delaunay triangulation of the nodes
def delaunay_graph(nodes):
	edges = []
	points = np.array(nodes)
	tri = Delaunay(points)
	simplices = tri.simplices
	triangles = points[simplices].tolist()
	for triangle in triangles:
		edges.append((tuple(triangle[0]), tuple(triangle[1]), hypot(triangle[0][1] - triangle[1][1], triangle[0][0] - triangle[1][0])))
		edges.append((tuple(triangle[1]), tuple(triangle[2]), hypot(triangle[1][1] - triangle[2][1], triangle[1][0] - triangle[2][0])))
		edges.append((tuple(triangle[2]), tuple(triangle[0]), hypot(triangle[2][1] - triangle[0][1], triangle[2][0] - triangle[0][0])))
	return edges

def full_graph(nodes):
	edges = []
	print "Time to get full graph!"
	while(len(nodes) != 0):
		current_node = nodes.pop(0)
		current_y = current_node[0]
		current_x = current_node[1]

		for i in range(len(nodes)):
			temp_node = nodes[i]
			temp_y = temp_node[0]
			temp_x = temp_node[1]
			
			weight = hypot(current_x - temp_x, current_y - temp_y)
			edges.append((current_node, temp_node, weight))
	return edges # Return tuple of (node_1, node_2, distance)

# Parallelize this to N threads
def min_span_tree(nodes):

	# Edges that make up the min spanning tree
	span_tree = []

	# Make forest of trees (list of nodes) with single node per tree
	forest = [[] for x in xrange(len(nodes))]
	for i in range(len(nodes)):
		forest[i].append(nodes[i])

	print "Finished the forest"

	# Get all edges in a fully connected graph of the nodes and sort edges
	#edges = full_graph(nodes)
	edges = delaunay_graph(nodes)
	print "Got delaunay graph!"

	# Sort edges by weight
	sorted_edges = sorted(edges, key=lambda edge: edge[2]) 
	
	print "Sorted delaunay graph"
	# Iterate through all edges (until we're done)
	for edge in sorted_edges:

		# We're done! All nodes in one tree
		if len(forest) == 1:
			break

		node_a = edge[0]
		node_b = edge[1]

		a_index = -1
		b_index = -1

		# Go through forest and find which tree node a and b are located
		for i in range(len(forest)):

			tree = forest[i]

			if node_a in tree:
				a_index = i

			if node_b in tree:
				b_index = i

			if (a_index != -1) and (b_index != -1):
				break

		# They're in different trees! Great; let's join them
		if a_index != b_index:
			forest[a_index] = forest[a_index] + forest[b_index]
			forest.pop(b_index)
			span_tree.append(edge)

		# Else: They're already in the same tree; don't care

	return span_tree

#Make tree from edges, and then do a depth first search
def depth_first_search(edges):

	graph = dict()

	#Go through all edges and construct graph in dictionary
	for edge in edges:
		node_a = edge[0]
		node_b = edge[1]

		if node_a in graph:
			graph[node_a].append(node_b)
		else:
			graph[node_a] = [node_b]

	#Pick arbitrary node and call it root
	root_node = graph[graph.keys()[0]]

	root_children = graph[root_node]

	#Sort children by angle from 0 degrees (EAST) around counter-clockwise
	sorted_children = sorted(root_children, key=lambda child: edge_angle((root_node, child))) 

	


# Find the angle of the edge
def edge_angle(edge):
	x1 = edge[0][0]
	y1 = edge[0][1]

	x2 = edge[1][0]
	y2 = edge[1][1]

	temp = atan2(y2 - y1, x2 - x1) * (180 / pi)

	if temp < 0:
		temp += 360
	return temp
