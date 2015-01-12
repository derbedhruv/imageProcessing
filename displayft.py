# This shall display the FT of an image, after converting it to greyscale
# FIRST al the declarations...
imageName = "images/fpm_artificial/01.png"

import numpy, Image, pylab, matplotlib.cm as cm

# Now we begin the fun...
im = Image.open(imageName).convert("L")		# L makes it greyscale
image = numpy.array(im)		# convert to numpy array

f = numpy.fft.fftshift(numpy.fft.fft2(image))		# 2D fft done, just like MATLAB, also shifted yo

# this segment just displays the plain old ft..
psd = numpy.abs(f)

pylab.figure()
pylab.imshow(image, cmap = cm.Greys_r)		# display in greyscale space

pylab.figure()
pylab.imshow(numpy.log10(psd+1))
pylab.show()
