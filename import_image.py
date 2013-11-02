import Image
import numpy

# Read in image and convert to grayscale
img = Image.open('rotunda.jpeg')
img_2 = i.convert('L')    #convert to grayscale
array = numpy.asarray(img_2)

# Give output array dimmensions
out_array = numpy.zeros(array.size).reshape((len(array), len(array[0])))

# Iterate through 2d array and invert values
for i in range(len(array)):
	for j in range(len(array[0])):
		out_array[i][j] = 1 - array[i][j]

# Convert array to image
out_img = Image.fromarray(array.astype(numpy.uint8))
out_img.save('img2.png')
