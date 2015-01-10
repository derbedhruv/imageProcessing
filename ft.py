# This shall display the Fourier transform of an image. Really simple code
# FIRST al the declarations...
imageName = "cos1.png"

from scipy import fftpack
import numpy, Image, pylab

# There's no inbuilt function in any of these python libraries to convert from rgb to grayscale
# This one was taken from http://stackoverflow.com/questions/12201577/convert-rgb-image-to-grayscale-in-python
def rgb2gray(rgb):
    # obv rgb has to be a numpy array
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

# Now we begin the fun...
im = Image.open(imageName)
image = numpy.array(im)		# convert to numpy array

print(image.shape)
print(image.size)

# image = rgb2gray(image)

f = fftpack.fft2(image)		# 2D fft done, just like MATLAB

f = fftpack.fftshift(f)		# again like MATLAB, shift the origin to the 'center'

psd = numpy.abs(f)

pylab.imshow(numpy.log10(psd + 1))
pylab.show()
