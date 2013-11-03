#!/usr/bin/python

# test_drawing.py 
# Test harness for drawing functionality
# 
# Author: Tommy Tracy II 
# Created: 11/2/2013
#

import Image
import numpy
import sys
import drawing

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

a = []
# Make some example stipples
for i in range(2, len(array)-2, 10):
	for j in range(2, len(array[0])-2, 10):
		a.append((i, j))		

out_img = drawing.draw_stipples(img_2, a, 2)

# Give output array dimmensions
#out_array = numpy.zeros(array.size).reshape((len(array), len(array[0])))

# Convert array to image and write to output file
#out_img = Image.fromarray(out_array.astype(numpy.uint8))
out_img.save(out_filename)
	
