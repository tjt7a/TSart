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
#./import_image.py <inputfile> <outputfile>
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
out_img.save("temp.jpeg")

# Call stipple.py

stipples = stipple.stipple(out_array, 0.08, 0, 9)
#print stipples[0]
#print "-----"
print "blocks = ",stipples[1]
print "recursions = ",stipples[2]
print "stipple number = ",stipples[3]
out_img = Image.new('L', (len(array[0]), len(array)), "white")
out_img = drawing.draw_stipples(out_img, stipples[0], 1)
out_img.save("post_stipple.jpeg")
print "Finished drawing stipples"
edges = graph.min_span_tree(stipples[0])
print "Got edges"
out_img = drawing.draw_edges(out_img, edges)
print "Drew edges"
out_img.save(out_filename)