# This file shall operate on the usaf target image, in which it is known that the dimensions are 1.58 microns/pixel
# With this knowledge, we will try to remove certain spatial frequencies along particular directions (x/y) to verify that this is correct
# This will go a long way in correlating the wavevectors in the ultimate fpm project to the fourier transform dimensions.

import Image, numpy, pylab, matplotlib.cm as cm

## GLOBAL DEFINITIONS
pixel_size = 3.45	# actual dimension of camera sensor pixel
pi = 3.141592
magnification = 2.	

# size of object we want to resolve
object_size = 20.0	# microns
print(object_size)
print("microns")

u = Image.open("./data/20150319_fpm/USAF_1_2X_lightLevel6.jpg").convert("L")

usaf = numpy.array(u)
usaf_width = usaf.shape[0]
usaf_height = usaf.shape[1]

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

def gaussian(x, offset, fwhm):
  # this one's taken and modified from http://stackoverflow.com/questions/14873203/plotting-of-1-dimensional-gaussian-distribution-function
  # 'x' is the 1-D space on which the gaussian function will be applied
  sig = fwhm/2.3548   # relating sigma and the FWHM http://mathworld.wolfram.com/GaussianFunction.html
  return (1./sig*numpy.power(2.*numpy.pi, 0.5))*numpy.exp(-numpy.power(x - offset, 2.) / (2. * numpy.power(sig, 2.)))

def gaussian_filter(centre, shape, width, h_max):
  # a 2d gaussian at centre (a tuple) and with width in both dimensions as 'width', with height h_max
  # The shape of the numpy array thus generated would be of shape 'shape' (tuple)
  x,y = numpy.ogrid[:shape[0],:shape[1]]
  gx = h_max*gaussian(x, shape[0]/2, width)
  gy = h_max*gaussian(y, shape[1]/2, width)

  return gx*gy


# next we define a band stop filter function ... which is just two circular masks of radius slightly higher and slightly lower than 
# a particular frequency.. we will have two arguments, the "freqency" to stop and the spread of the frequency.
def band_stop(target_image, freq, spread):
  # find the center coordinates of the target_image
  center = [target_image.shape[0]/2, target_image.shape[1]/2]
  
  # convert the 'frequency' into pixels
  nyquist_freq = 1.00/(2*pixel_size)		# units of micron-1, this is the max freqyency which can be resolved by this fft
  frequency = (1/magnification)*(freq/nyquist_freq)*(target_image.shape[1]/2)	
  
  # define two circular masks with radius (frequency - spread) and (frequency + spread)
  # inner = circular_mask(target_image.shape, center, (frequency - spread))
  # outer = circular_mask(target_image.shape, center, (frequency + spread))

  ## now apply these masks and generate the target fourier transform
  # first we find the fourier transform
  f = numpy.fft.fftshift(numpy.fft.fft2(target_image))
  
  # then we add together the result of applying both masks
  band_stopped_fft = numpy.copy(f)

  #f_inner = numpy.copy(f)
  # band_stopped_fft[outer] = 0
  # f_inner[inner] = 0
  # f_inner = f - f_inner
  # band_stopped_fft = band_stopped_fft + f_inner
  # band_stopped_fft = f - band_stopped_fft
  
  bs_filt = gaussian_filter(center, target_image.shape, frequency, 1) # 2*freq because it is symmetrical about the center and we're giving the spread
  band_stopped_fft = band_stopped_fft*bs_filt

  # display it so we know it's all good..
  pylab.figure()
  p = numpy.log(numpy.abs(band_stopped_fft) + 1)
  # p = numpy.log(numpy.abs(f_inner) + 1)
  pylab.imshow(p, cmap=cm.Greys_r)

  # then calculate the inverse fft of it and return..
  band_stopped_image = numpy.abs(numpy.fft.ifft2(numpy.fft.fftshift(band_stopped_fft)))
  
  # we then normalize all the values to (0,255)
  band_stopped_image = 255*band_stopped_image/(numpy.max(band_stopped_image))

  # return it..
  return band_stopped_image

## now the section where we apply everything..

# calculating the frequency corresponding to the object size we need...
object_frequency = 1.00/(2*object_size)		# again in micron-1

# then apply the circular frequency mask..
final_image = band_stop(usaf, object_frequency, 1)
final = Image.fromarray(final_image.astype(numpy.uint8))

# then display the filtered image
pylab.figure()
pylab.imshow(final, cmap=cm.Greys_r)
pylab.show()
