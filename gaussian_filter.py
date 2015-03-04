# this will plot a gaussian function and then we shall convert this into a lowpass filter with precisely known cutoff

import numpy, matplotlib.cm as cm, pylab

# this one's taken and modified from http://stackoverflow.com/questions/14873203/plotting-of-1-dimensional-gaussian-distribution-function

def gaussian(x, offset, fwhm):
  # 'x' is the 1-D space on which the gaussian function will be applied
  sig = fwhm/2.3548   # relating sigma and the FWHM http://mathworld.wolfram.com/GaussianFunction.html
  return (1/sig*numpy.power(2*numpy.pi, 0.5))*numpy.exp(-numpy.power(x - offset, 2.) / (2 * numpy.power(sig, 2.)))

def gaussian_filter(centre, shape, width, h_max):
  # a 2d gaussian at centre (a tuple) and with width in both dimensions as 'width', with height h_max
  # The shape of the numpy array thus generated would be of shape 'shape' (tuple)
  x,y = numpy.ogrid[:shape[0],:shape[1]]
  gx = h_max*gaussian(x, shape[0]/2, width)
  gy = h_max*gaussian(y, shape[1]/2, width)

  return gx*gy

shape = [100,100]
width = 10
center = [shape[0]/2, shape[1]/2]
h_max = 1
 
pylab.figure()
pylab.imshow(gaussian_filter(center, shape, width, h_max), cmap=cm.Greys_r)
pylab.show()

# plt.plot(t, gaussian(t, 0., 1))
# plt.plot(x, gx)
# plt.show()