#!/usr/bin/python

# import_image.py - Image importer 
#
# Author: Tommy Tracy II 
# Created: 11/2/2013
#

import Image
import ImageEnhance
import numpy
import sys
import stipple
import drawing
import graph

#Syntax:
#./import_image.py <inputfile> <outputfile> <exponent for contrast adjustments> <lower histogram window> <higher histogram window>
if(len(sys.argv) != 6):
	print "ERROR: provide input and output file names"
	exit()

# Set input and output file names
in_filename = sys.argv[1] 
out_filename = sys.argv[2]
exponent = float(sys.argv[3]) #exponent from 0 ->. If < 1, sublinear, if > 1, superlinear
histogram_edges = (int(sys.argv[4]), int(sys.argv[5]))

# Catch incorrect input filename
try:
	img = Image.open(in_filename)
except IOError:
	print "File:\'", in_filename, "\' doesn't exist"
	exit()

# Convert to grayscale and then to array
img_2 = img.convert('L')

array = numpy.asarray(img_2)

# Generate look up table for mapping intensities to exponential curve
# window between min and max intensity
look_up_table = []																
for i in range(0, (histogram_edges[0]+1)):
	look_up_table.append(0)
for i in range(histogram_edges[0], (histogram_edges[1]+1)):
	look_up_table.append(255 * ((i-histogram_edges[0])**exponent)/((histogram_edges[1])**exponent))
for i in range(histogram_edges[1], 256):
	look_up_table.append(255)


# Give output array dimmensions
out_array = numpy.zeros(array.size).reshape((len(array), len(array[0])))

for i in range(len(array)):
	for j in range(len(array[0])):
		out_array[i][j] =  look_up_table[array[i][j]]

out_img = Image.fromarray(out_array.astype(numpy.uint8))
out_img.save("pre_stipple.jpeg")

# Call stipple.py

# stipple.stipple(<image array> , <variance>, <min size of minimum array chunk>)
stipples = stipple.stipple(out_array, 0.1, 0, 64)

print "blocks = ",stipples[1]
print "recursions = ",stipples[2]
print "stipple number = ",stipples[3]

out_img = Image.new('L', (len(array[0]), len(array)), "white")
out_img = drawing.draw_stipples(out_img, stipples[0], 1)
out_img.save("post_stipple.jpeg")
print "Finished drawing stipples"

edges = graph.min_span_tree(stipples[0])

#
#for i in range(0, len(edges)-1):
#	for j in range(i+1, len(edges)):
#		if (edges[i][0] == edges[j][0]) and (edges[i][1] == edges[j][1]):
#			print "we're seeing shit again!"
#			print edges[i], edges[j]
#		if (edges[i][0] == edges[j][1]) and (edges[i][1] == edges[j][0]):
#			print "we're seeing shit again!"
#			print edges[i], edges[j]
#
#print "done"
#exit()

out_img = Image.new('L', (len(array[0]), len(array)), "white")
out_img = drawing.draw_edges(out_img, edges)
out_img.save("post_min_span_tree.jpeg")

tsp_edges = graph.depth_first_traversal(edges)

out_temp_img = Image.new('L', (len(array[0]), len(array)), "white")
out_temp_img = drawing.draw_edges(out_temp_img, tsp_edges)
out_temp_img.save("before_uncrossing.jpg")

#tsp_edges = list(set(tsp_edges))

#for i in range(0, len(tsp_edges)-1):
#	for j in range(i+1, len(tsp_edges)):
#		if (tsp_edges[i][0] == tsp_edges[j][0]) or (tsp_edges[i][1] == tsp_edges[j][1]):
#			print "DANGEROUS: DUPLICATE"
#			print tsp_edges[i]
#			print tsp_edges[j]

print "Got edges"
tsp_without_crossings = graph.remove_crossings(tsp_edges)

#print tsp_without_crossings
print "Done uncrossing!!"
out_img = drawing.draw_edges(out_img, tsp_without_crossings)
print "Drew edges"
out_img.save(out_filename)