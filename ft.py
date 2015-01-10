# This shall display the Fourier transform of an image. Really simple code
# FIRST al the declarations...
imageName = "eye.jpg"

import numpy, fftpack, Image, pylab

im = Image.open(imageName)
image = numpy.array(im)		# convert to numpy array

# print(image.shape)
# print(image.size)

f = fftpack.fft2(image)		# 2D fft done, just like MATLAB

f = fftpack.fftshift(f)		# again like MATLAB, shift the origin to the 'center'

psd = abs(f)

pylab.imshow(numpy.log10(psd)
pylab.show()
