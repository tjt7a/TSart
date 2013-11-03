#!/usr/bin/python

# import_image.py - Image importer 
#
# Author: Tommy Tracy II 
# Created: 11/2/2013
#

import Image
import numpy
import sys

#Syntax:
#./import_image.py <inputfile> <outputfile>
if(len(sys.argv) != 3):
	print "ERROR: provide input and output file names"
	exit()

# Set input and output file names
in_filename = sys.argv[1] 
out_filename = sys.argv[2]

# Catch incorrect input filename
try:
	img = Image.open(in_filename)
except IOError:
	print "File:\'", in_filename, "\' doesn't exist"
	exit()

# Convert to grayscale and then to array
img_2 = img.convert('L') 
array = numpy.asarray(img_2)

# Give output array dimmensions
out_array = numpy.zeros(array.size).reshape((len(array), len(array[0])))

# Iterate through 2d array and invert values
for i in range(len(array)):
	for j in range(len(array[0])):
#		if(((j > len(array[0])/2) and (i < len(array)/2)) or ((j < len(array[0])/2) and (i > len(array)/2))):		
#			out_array[i][j] = 1 - array[i][j]
#		else:
#			out_array[i][j] = array[i][j]
		if((i%(len(array)/100)==0) or (j%(len(array[0])/100)==0)):
			out_array[i][j] = 1
		else:
			out_array[i][j] = array[i][j]

# Convert array to image and write to output file
out_img = Image.fromarray(out_array.astype(numpy.uint8))
out_img.save(out_filename)
