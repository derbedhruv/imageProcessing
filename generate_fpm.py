# This shall generate the "artificial fpm" files from the eye.jpg image, and save them accordingly. 
# These will then be analyzed later and then stitched together to get a higher res image
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
im = Image.open(imageName)	# full colour yo

# we display the source image first..
'''
pylab.figure()
pylab.imshow(im)
'''

image = numpy.array(im)		# convert to numpy array
final_image = numpy.zeros(image.shape)	# empty array for our final image
# print('final image shape - ', final_image.shape)

### we will generate 6 different images from this one and save them all with names from 00 to 22, by shifting a circular pupil of the FT by 
### 50 units back and forth.
### enter the number of shifted images desired along each axis...
xax = 3 
yax = 3

radius = 100
cx = image.shape[0]/2
cy = image.shape[1]/2

fshift = 50

# and it shall be so!
for m in range(0, xax):
  for n in range(0, yax):

    print('building image ' + str(m) + ',' + str(n) + ' with the FT pupil shifted by ' + str(fshift*(m - abs(xax/2))) + ',' + str(fshift*(n - abs(yax/2))))

  ## Hear ye hear ye, this is for splitting shit up into RGB components and then performing individual operations on them yo
  # now we split the image into it's red, green and blue arrays
    for i in range(0, image.shape[2]):				# for some reason if you put range(0,2) it screws the colours up. WHY
      channel = image[:,:,i]					# split out the channel
      f = numpy.fft.fftshift(numpy.fft.fft2(channel))		# find 2D FFT
      # now you can perform some shit on the fourier transform ..
      # this section chops out a section and displays the modified file
      # first the center coordinates..

      mask = circular_mask(image.shape, (cx + fshift*(m - abs(xax/2)), cy + fshift*(n - abs(yax/2))), radius)
      f[~mask] = 0					# chop out circular section
      psd = numpy.abs(f)					# could be either, assuming the transforms are hte same for each chan
  
      # now we find the inverses and stitch them together
      final_image[:,:,i] = numpy.fft.ifft2(numpy.fft.fftshift(f))

    image_modi = Image.fromarray(final_image.astype(numpy.uint8))	# this is still giving complex values, why?
    image_modi.save('./images/fpm_artificial/' + str(m) + str(n) + '.png')

    pylab.figure()
    pylab.imshow(image_modi)		# display in colour space

  pylab.figure()
  pylab.imshow(numpy.log10(psd+1))

# pylab.show()
