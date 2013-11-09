import numpy as np

# Stipple
### image - Image array
### density - Stipples per 
def stipple(image, density, var, min_size):
	# Check base cases
	### If variation of image is below threshold
	if(np.var(image) < var):
		output = calc_vectors(image, density)
		return (output[0], 1, 1, output[1])
	### If size of the sub-block is below minimum size
	if(len(image)*len(image[0]) < min_size):
		output = calc_vectors(image, density)
		return (output[0], 1, 1, output[1])

	# Get image width and length, and vertical and horizontal splits
	image_w = len(image[0])
	image_l = len(image)
	vert_split = int(np.ceil(image_l/2.0))
	horiz_split = int(np.ceil(image_w/2.0))

	# Get sub-block images
	nw_image = image[0:vert_split,0:horiz_split]
	ne_image = image[0:vert_split,(horiz_split-1):image_w]
	sw_image = image[(vert_split-1):image_l,0:horiz_split]
	se_image = image[(vert_split-1):image_l,(horiz_split-1):image_w]
	# Call stipple recursively
	nw_vect = stipple(nw_image, density, var, min_size)
	ne_vect = stipple(ne_image, density, var, min_size)
	sw_vect = stipple(sw_image, density, var, min_size)
	se_vect = stipple(se_image, density, var, min_size)

	# Convert sub-block vectors to super-block vectors
	shift_vect(ne_vect[0], (horiz_split-1), 0)
	shift_vect(sw_vect[0], 0, (vert_split-1))
	shift_vect(se_vect[0], (horiz_split-1), (vert_split-1))

	blocks = nw_vect[1] + ne_vect[1] + sw_vect[1] + se_vect[1]
	recursions = nw_vect[2] + ne_vect[2] + sw_vect[2] + se_vect[2] + 1
	num_stipples = nw_vect[3] + ne_vect[3] + sw_vect[3] + se_vect[3]
	
	return ((nw_vect[0] + ne_vect[0] + sw_vect[0] + se_vect[0]), blocks, recursions, num_stipples)


def shift_vect(vect, x_offset, y_offset):
	output = []
	for i in range(len(vect)):
		vect[i] = (vect[i][0] + y_offset, vect[i][1] + x_offset)
	return vect


def calc_vectors(image, density):

	# Get the expected pixel value from the image
	shading = 255 - np.mean(image)
	stip_ratio = (shading*density)/255.0
	#print "mean = ",np.mean(image)
	#print "shading = ",shading/255.0
	#print "density = ",density
	#print "stip_ratio = ",stip_ratio

	# Determine number of random stipples for image
	area = len(image)*len(image[0])
	num_stipples = int(round(area*stip_ratio))

	# Create vectors and return
	randx = np.random.randint(0, len(image[0]), num_stipples)
	randy = np.random.randint(0, len(image), num_stipples)
	output = zip(randy, randx)
	return (output, num_stipples)
