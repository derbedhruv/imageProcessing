# THis file shall stitch together the small images in the fourier domain and produce a higher res image
# Remember the images are such (2D fourier domain) ..
# 
# 	02  12  22
# 	01  11  21
#	00  10  20
#
# Where each step indicates a step in 50 in the fourier domain. Remember that 11 is the actual (0,0).
import numpy, pylab, Image, scipy.misc

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


#### So we'll start by upsampling the one we know is the 'central' one, i.e. who's FT circular mask is in the center
####
folder = "./images/fpm_artificial/"	# the folder where the files of the name given above lie..
filetype = ".jpg"

central_image = Image.open(folder + '00' + filetype)
ncentral = numpy.array(central_image)

'''
pylab.figure
pylab.imshow(central_image)
'''

# now the actual upsampling..2 times the size
upsampled = scipy.misc.imresize(ncentral, (3072, 4096))
upsampled_guess_image = Image.fromarray(upsampled)

'''
# and we show it
pylab.figure
pylab.imshow(upsampled_guess_image)
'''

# and we save it
# upsampled_guess_image.save(folder + 'upsampled' + filetype)

# we find its fourier transform(s) and keep them handy
upsampled_ft = numpy.zeros(upsampled.shape)
for j in range(0, upsampled.shape[2]):
  up_channel = upsampled[:,:,j]
  upsampled_ft[:,:,j] = numpy.fft.fftshift(numpy.fft.fft2(up_channel))

# pylab.show()

#### C'est l'heure.
## First we create 2 masks. One which will be a standard central circular mask and the other with variable center, corresponding to 
## the particular picture.
radius = 100
fshift = 50

xmax = 2
ymax = 1

for p in range(0, xmax):
  for q in range(0, ymax):
     # open figure
     im = Image.open(folder + str(p) + str(q) + filetype)
     image = numpy.array(im)
     
     cx = image.shape[0]/2
     cy = image.shape[1]/2
     
     # first we create the central mask that will extract the center of the shifted fft of the image
     center_circle = circular_mask(image.shape, (cx, cy), radius )
     
     # then the shifted circular pupil based on (p,q)
     shifted_circle = circular_mask(image.shape, (((upsampled.shape[0]/2)) + fshift*(p - abs(xmax/2)), (upsampled.shape[1]/2) + fshift*(q - abs(ymax/2))), radius)
     
     for i in range(0, image.shape[2]):
       channel = image[:,:,i]
       f = numpy.fft.fftshift(numpy.fft.fft2(channel))
       
       # the magic sauce: replacing the circular chunk of the upsampled image's FT with that from the lowres image
       # upsampled_ft[:,:,i][shifted_circle] = f[center_circle]
       
       
# then we take the ifft and build the upsampled image again..
highres_image = numpy.zeros(upsampled.shape)
for a in range(0, 3): 
  highres_image[:,:,a] = numpy.fft.ifft2(numpy.fft.fftshift(upsampled_ft[:,:,a])) 

highres_output_image = Image.fromarray(highres_image.astype(numpy.uint8))

pylab.figure()
pylab.imshow(highres_output_image)
pylab.show()
