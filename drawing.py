#!/usr/bin/python

# drawing.py 
# Image Drawing Module for TSP Art 
# 
# Author: Tommy Tracy II 
# Created: 11/2/2013
#


import Image
import numpy
import ImageDraw

def draw_stipples(img, stipples, radius):
	draw = ImageDraw.Draw(img)
	r = radius
	for i in stipples:
		y = i[0]
		x = i[1]
		draw.ellipse((x-r, y-r, x+r, y+r), fill=0)
	return img 

def draw_edges(img, edges):
	draw = ImageDraw.Draw(img)
	for edge in edges:
		y1 = edge[0][1]
		x1 = edge[0][0]

		y2 = edge[1][1]
		x2 = edge[1][0]
		draw.line((y1, x1, y2, x2), fill = 0)
	return img	
