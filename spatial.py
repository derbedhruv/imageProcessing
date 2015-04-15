# This will convert from the spatial domain to the 2D-spatial frequency domain. 
# THis is the key step in the fourier ptychographic microscopy algorithm
import numpy, Image, matplotlib, pylab, scipy.misc

# First we get imaging parameters
fileName = '/home/derbedhruv1/Documents/fpm/imageProcessing/data/20150319_fpm/USAF_1_2X_lightLevel6.jpg'	# image location 
pixel_size = 3.45	# pixel size in microns (actual), from the camera datasheet
magnification = 2	# How many times the image is magnified w.r.t. the object
scale = 5 

# Next we read in the image into an array
image = Image.open(fileName).convert("L")
image = numpy.array(image)	
M,N = image.shape		# These are the original image dimensions
upsampled = scipy.misc.imresize(image, [scale*M, scale*N])

# Now the fourier transform
# ft = numpy.fft.fftshift(numpy.fft.fft2(upsampled))
# A,B = ft.shape
A = scale*M
B = scale*N

px = pixel_size/magnification	# microns/pixel
spatial_freq = 1./(M*(px/scale))	# micron-1/pixel
print("one pixel is " + str(spatial_freq) + " micron-1") 

print("x-frequency limits in spatial frequencies (micron-1) = " + str(-A*spatial_freq/2) + ", " + str((A-1)*spatial_freq/2) + "mapped to " + str(-A/2) + ", " + str((A-1)/2))

pupil = 2*numpy.pi*0.06/0.632	# micron-1
print("and the radius of the MTF of the lens is = " + str(pupil) + " micron-1 or " + str(pupil/spatial_freq))

'''
# each frequency step corresponds to 
px = pixel_size/magnification	# microns/pixel
deltaF = 1/(2*px*M)

# The frequency limits which we see in the plotted FFT are
'''
