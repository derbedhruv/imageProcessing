# This shall display the Fourier transform of an image. BUT IN COLOUR BITCHES
# FIRST al the declarations...
imageName = "images/eye.jpg"

import numpy, Image, pylab, matplotlib.cm as cm

# the circular_mask was copied from http://stackoverflow.com/questions/18352973/mask-a-circular-sector-in-a-numpy-array
def circular_mask(shape,centre,radius):
    """
    Return a boolean mask for a circular sector. The start/stop angles in  
    `angle_range` should be given in clockwise order.
    """
    angle_range = [0,360]

    x,y = numpy.ogrid[:shape[0],:shape[1]]
    cx,cy = centre
    tmin,tmax = numpy.deg2rad(angle_range)

    # ensure stop angle > start angle
    if tmax < tmin:
            tmax += 2*numpy.pi

    # convert cartesian --> polar coordinates
    r2 = (x-cx)*(x-cx) + (y-cy)*(y-cy)
    theta = numpy.arctan2(x-cx,y-cy) - tmin

    # wrap angles between 0 and 2*pi
    theta %= (2*numpy.pi)

    # circular mask
    circmask = r2 <= radius*radius

    # angular mask
    anglemask = theta <= (tmax-tmin)

    return circmask*anglemask

# Now we begin the fun...
im = Image.open(imageName)	# L makes it greyscale
image = numpy.array(im)		# convert to numpy array

'''
pylab.figure()
pylab.imshow(image)

print(image.shape)
print(image.size)
'''

f = numpy.fft.fftshift(numpy.fft.fft2(image))		# 2D fft done, just like MATLAB

# this segment just displays the plain old ft..
# f = fftpack.fftshift(f)		# again like MATLAB, shift the origin to the 'center'

'''
pylab.figure()
pylab.imshow(numpy.log10(psd+1))
pylab.show()
'''

# this section chops out a section and displays the modified file
mask = circular_mask(image.shape, (image.shape[0]/2, image.shape[1]/2), 600)
# f[~mask] = 0		# chop out circular section
psd = numpy.abs(f)

imm = numpy.fft.ifft2(numpy.fft.fftshift(f))
image_modi = Image.fromarray(imm.astype(numpy.uint8))	# this is still giving complex values, why?

pylab.figure()
pylab.imshow(image_modi)		# display in colour space

pylab.figure()
pylab.imshow(numpy.log10(psd+1))
pylab.show()
