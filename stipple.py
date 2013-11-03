import numpy as np

def stipple(image, grid_size, var, min_size):
	# Check base cases
	if(np.var(image) < var):
		return [(len(image[0])-1)/2, (len(image)-1)/2]
	if(len(image)*len(image[0]) < min_size):
		return [(len(image[0])-1)/2, (len(image)-1)/2]

	
