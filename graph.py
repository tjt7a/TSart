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

VERBOSE = False

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
	if VERBOSE:
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

	if VERBOSE:
		print "Finished the forest"

	# Get all edges in a fully connected graph of the nodes and sort edges
	#edges = full_graph(nodes)
	edges = delaunay_graph(nodes)
	
	if VERBOSE:
		print "Got delaunay graph!"

	# Sort edges by weight
	sorted_edges = sorted(edges, key=lambda edge: edge[2]) 
	
	if VERBOSE:
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
def depth_first_traversal(edges):

	graph = dict()

	# Go through all edges and construct graph in dictionary
	# This graph will need to be bi-directional
	# Cannot guarantee full traversal otherwise

	for edge in edges:
		node_a = edge[0]
		node_b = edge[1]

		if node_a in graph:
			graph[node_a].append(node_b)
		else:
			graph[node_a] = [node_b]

		if node_b in graph:
			graph[node_b].append(node_a)
		else:
			graph[node_b] = [node_a]

	# Pick arbitrary node and call it root
	root_node = graph[graph.keys()[0]][0]

	# Iteratively traverse it
	# Order children and traverse in a counter-clockwise order, printing out new verticies as we reach them
	tsp_nodes = pre_order(root_node, graph)	

	#Chain the nodes into a series of edges!
	tsp_edges = []
	for i in range(0, (len(tsp_nodes)-1)):
		tsp_edges.append((tsp_nodes[i], tsp_nodes[i+1]))
	tsp_edges.append((tsp_nodes[len(tsp_nodes)-1], tsp_nodes[0]))

	return tsp_edges


def pre_order(root_node, graph):
	
	if VERBOSE:
		print "Root: ", root_node
	
	tsp_nodes = [] # Add nodes to the tsp_nodes list as we visit them in the depth-first traversal
	tsp_nodes.append(root_node) # Add root node as the first node on the tsp path

	parent_stack = [] # Stack to push on parents as we move down the tree

	parent = root_node # Root will be our first parent!
	old_parent = root_node

	while True:

		# Grab the chidren from GRAPH
		children = graph[parent]

		# Remove parent's parent from children
		if old_parent in children:
			children.remove(old_parent)

		if VERBOSE:
			print "parent: ", parent
			print "parent stack: ", parent_stack

		# If we've popped everyone off the stack and we're out of children, time to return
		if (len(parent_stack) == 0) and (len(children) == 0):
			if VERBOSE:
				print "Out of stack and Children"
			break

		# Order the children by location (starting at 0 degrees, going counter-clocksise)
		sorted_children = sorted(children, key=lambda child: edge_angle((parent, child)))
		if VERBOSE:
			print "Sorted Children: ", sorted_children

		# If we're out of children, go up one!
		if len(sorted_children) == 0:
			parent = parent_stack.pop()
			if VERBOSE:
				print "No children, so pop"
			continue
		else:
			graph[parent].remove(sorted_children[0])
			old_parent = parent
			parent_stack.append(old_parent)
			parent = sorted_children[0]
			if VERBOSE:
				print "New Parent: ", parent
			tsp_nodes.append(parent) # Add node to the first position of the tsp_nodes list

	return tsp_nodes

# Detect a crossing
# The easiest way to do this is use the following rule:
# In order for two line segments to cross:
#	Both of Line segment 1's points must be on opposite sides of Line Segment 2
#	Both of Line segment 2's points must be on opposite sides of Line Segment 1
def detect_crossing(edge_1, edge_2):

	# Check if edge_2's points are on opposite sides of edge_1 (cross product)
	cross_1 = cross_product(edge_1, edge_2[0]) # Find cross product of edge_1 and first point of edge_2
	cross_2 = cross_product(edge_1, edge_2[1]) # Find cross product of edge_1 and second point of edge_2

	# If edge_2's points are on opposite sides of edge_1...
	if((cross_1 < 0 and cross_2 > 0) or (cross_1 > 0 and cross_2 < 0)):
	
		# Check if edge_1's points are on opposite sides of edge_2 (cross product)
		cross_3 = cross_product(edge_2, edge_1[0]) # Find cross product of edge_2 and first point of edge_1
		cross_4 = cross_product(edge_2, edge_1[1]) # Find cross product of edge_2 and second point of edge_1

		# If edge_1's points are on opposite sides of edge_2, return True - We found a crossing! :(
		if((cross_3 < 0 and cross_4 > 0) or (cross_3 > 0 and cross_4 < 0)):
			return True

	# Else, no crossing
	return False


# ---------- Fun Maths formulas --------- #

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

# Calculate the cross product  of the edge (edge[0], edge[1]) with another edge composed with the point (edge[0], point)
def cross_product(edge, point):
	return (edge[1][0] - edge[0][0]) * (point[1] - edge[0][1]) - (edge[1][1] - edge[0][1])*(point[0] - edge[0][0])