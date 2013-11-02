import Image
import numpy

# Read in image and convert to grayscale
img = Image.open('rotunda.jpeg')
img_2 = img.convert('L')    #convert to grayscale
array = numpy.asarray(img_2)

# Give output array dimmensions
out_array = numpy.zeros(array.size).reshape((len(array), len(array[0])))

# Iterate through 2d array and invert values
for i in range(len(array)):
	for j in range(len(array[0])):
		if(((j > len(array[0])/2) and (i < len(array)/2)) or ((j < len(array[0])/2) and (i > len(array)/2))):		
			out_array[i][j] = 1 - array[i][j]
		else:
			out_array[i][j] = array[i][j]

# Convert array to image
out_img = Image.fromarray(out_array.astype(numpy.uint8))
out_img.save('img2.png')
