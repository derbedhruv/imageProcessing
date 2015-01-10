# This shall display the Fourier transform of an image. Really simple code
# FIRST al the declarations...
imageName = "cos1.png"

from scipy import fftpack
import numpy, Image, pylab

im = Image.open(imageName)
image = numpy.array(im)		# convert to numpy array

print(image.shape)
print(image.size)

f = fftpack.fft2(image)		# 2D fft done, just like MATLAB

f = fftpack.fftshift(f)		# again like MATLAB, shift the origin to the 'center'

psd = numpy.abs(f)

pylab.imshow(numpy.log10(psd + 1))
pylab.show()
