#!/usr/bin/python

# import_image.py - Image importer 
#
# Author: Tommy Tracy II 
# Created: 11/2/2013
#

import Image
import numpy
import sys
import stipple
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

# Give output array dimmensions
out_array = numpy.zeros(array.size).reshape((len(array), len(array[0])))

# Call stipple.py

stipples = stipple.stipple(array, 0.005, 0, 256)
print "blocks = ",stipples[1]
print "recursions = ",stipples[2]
print "stipple number = ",stipples[3]
img_3 = Image.new('L', (len(array[0]), len(array)), "white")
out_img = drawing.draw_stipples(img_3, stipples[0], 2)
out_img.save(out_filename)
