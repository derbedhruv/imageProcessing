# This will perform a histogram equalization
# taken from http://www.janeriksolem.net/2009/06/histogram-equalization-with-python-and.html
import numpy

def histeq(im,nbr_bins=256):
  imhist,bins = numpy.histogram(im.flatten(),nbr_bins,normed=True)
  cdf = imhist.cumsum() #cumulative distribution function
  cdf = 255 * cdf / cdf[-1] #normalize
  im2 = numpy.interp(im.flatten(),bins[:-1],cdf)
  return im2.reshape(im.shape), cdf

