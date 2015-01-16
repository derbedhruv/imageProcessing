# THis file shall stitch together the small images in the fourier domain and produce a higher res image
# Remember the images are such (2D fourier domain) ..
# 
# 	02  12  22
# 	01  11  21
#	00  10  20
#
# Where each step indicates a step in 50 in the fourier domain. Remember that 11 is the actual (0,0).
import numpy, pylab, Image, scipy.misc, matplotlib.cm as cm

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
filename = "00"

print("reading image into array...")
central_image = Image.open(folder + filename + filetype)
ncentral = numpy.array(central_image)

print("finished. now will be upsampling the guess image...")

# now the actual upsampling..2 times the size
upsampled = scipy.misc.imresize(ncentral, (3072, 4096))

print("upsampling completed. Now will save it and then find the FT")

upsampled_guess_image = Image.fromarray(upsampled)

'''
pylab.figure()
pylab.imshow(upsampled_guess_image, cmap=cm.Greys_r)
'''
# and we save it
# upsampled_guess_image.save(folder + 'upsampled' + filetype)

# we find its fourier transform(s) and keep them handy
image_dimensions = len(upsampled.shape)
# upsampled_ft = numpy.zeros(upsampled.shape)
# upsampled_ft[:,:,j] = numpy.fft.fftshift(numpy.fft.fft2(up_channel))

if (image_dimensions == 3):
  upsampled_ft_r= numpy.fft.fft2(upsampled[:,:,0])
  upsampled_ft_g= numpy.fft.fft2(upsampled[:,:,1])
  upsampled_ft_b= numpy.fft.fft2(upsampled[:,:,2])
else:
  upsampled_ft = numpy.fft.fft2(upsampled)

print("FT of the upsampled image calculated and kept aside. Now will start adding the FTs of the lowres images one by one")

'''
pylab.figure()
pylab.imshow(numpy.log10(numpy.abs(upsampled_ft)+1))
'''
# pylab.show()

#### C'est l'heure.
## First we create 2 masks. One which will be a standard central circular mask and the other with variable center, corresponding to 
## the particular picture.
radius = 500
fshift = 250

xmax = 3
ymax = 3

for p in range(0, xmax):
  for q in range(0, ymax):
     # open figure
     print("stitching figure " + str(p) + "," + str(q) + "...")
     im = Image.open(folder + str(p) + str(q) + filetype)
     image = numpy.array(im)
     
     cx = image.shape[0]/2
     cy = image.shape[1]/2
     
     # first we create the central mask that will extract the center of the shifted fft of the image
     shifted_circle_lowres = circular_mask(image.shape, (((image.shape[0]/2)) + fshift*(p - abs(xmax/2)), (image.shape[1]/2) + fshift*(q - abs(ymax/2))), radius )
     
     # then the shifted circular pupil based on (p,q). Remember this will be applied to the higher res image
     shifted_circle = circular_mask(upsampled.shape, (((upsampled.shape[0]/2)) + fshift*(p - abs(xmax/2)), (upsampled.shape[1]/2) + fshift*(q - abs(ymax/2))), radius)
     
     # for i in range(0, 3):
     # channel = image[:,:,i]
     # image_ft = numpy.fft.fftshift(numpy.fft.fft2(channel))
     image_ft = numpy.fft.fftshift(numpy.fft.fft2(image))
       
     # the magic sauce: replacing the circular chunk of the upsampled image's FT with that from the lowres image
     # upsampled_ft[:,:,i][shifted_circle] = image_ft[center_circle]     
     upsampled_ft[shifted_circle] = image_ft[shifted_circle_lowres]     
     print("done!")
       
# then we take the ifft and build the upsampled image again..
highres_image = numpy.zeros(upsampled.shape)
# highres_image[:,:,a] = numpy.fft.ifft2(numpy.fft.fftshift(upsampled_ft[:,:,a])) 

print("last step, finding the ifft of the image and displaying..")

if (image_dimensions == 3):
  highres_image[:,:,0] = numpy.fft.ifft2(upsampled_ft_r)
  highres_image[:,:,1] = numpy.fft.ifft2(upsampled_ft_g)
  highres_image[:,:,2] = numpy.fft.ifft2(upsampled_ft_b)
else:
  highres_image = numpy.fft.ifft2(upsampled_ft)

highres_output_image = Image.fromarray(highres_image.astype(numpy.uint8))
# highres_output_image = Image.fromarray(abs(highres_image))
highres_output_image.save(folder + 'highresoutput' + filetype)

print("The high res output image has been saved at " + folder + 'highresoutput' + filetype)
'''
pylab.figure()
pylab.imshow(numpy.log10(numpy.abs(upsampled_ft)+1))

pylab.figure()
pylab.imshow(highres_output_image, cmap=cm.Greys_r)
pylab.show()
'''
