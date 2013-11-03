import Image
import numpy
import ImageDraw

def draw_stipples(img, stipples, radius):
	print stipples
	draw = ImageDraw.Draw(img)
	r = radius
	for i in stipples:
		x = i[0]
		y = i[1]
		draw.ellipse((x-r, y-r, x+r, y+r))
	return img 
