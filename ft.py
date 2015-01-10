# This shall display the Fourier transform of an image. Really simple code
# FIRST al the declarations...
imageName = "images/eye.jpg"

from scipy import fftpack
import numpy, Image, pylab

# There's no inbuilt function in any of these python libraries to convert from rgb to grayscale
# This one was taken from http://stackoverflow.com/questions/12201577/convert-rgb-image-to-grayscale-in-python
def rgb2gray(rgb):
    # obv rgb has to be a numpy array
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b

    return gray

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
im = Image.open(imageName)
image = numpy.array(im)		# convert to numpy array

# circular mask fun
mask = circular_mask(image.shape, (image.shape[0]/2, image.shape[1]/2), 300)
image[~mask] = 0

pylab.figure()
pylab.imshow(image)

print(image.shape)
print(image.size)

if (len(image.shape) == 3):
  # if it is an RGB image, convert to graysscale yo
  image = rgb2gray(image)

f = fftpack.fft2(image)		# 2D fft done, just like MATLAB

# this segment just displays the plain old ft..
f = fftpack.fftshift(f)		# again like MATLAB, shift the origin to the 'center'
psd = numpy.abs(f)
pylab.figure()
pylab.imshow(numpy.log10(psd+1))
pylab.show()

# this section chops out a section and displays the modified file


