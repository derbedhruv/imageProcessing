##
# Fourier Ptychographic Microscopy Imaging of known samples for increased resolution and FOV
#
# Author: Dhruv Joshi
#
#
# THis file shall stitch together the small images in the fourier domain and produce a higher res image
# This is based on work reported by Zheng et al in Nature Photonics 7.9 (2013), 739-745
# 
# Images were taken on an Olympus BX51 fluorescence microscope with a 2X Plan N achromat wide angle wide FOV lens with NA of 0.06
# This is a small NA and I am not sure if this is the NA of the entire optical system. This will have to be researched. 
# 
# The illumination of the system was done as follows: (the row-column numbers are exact)
# 
# 00 10 20 | 40 50 60 70 
# 01 11 21 | 41 51 61 71
# ---------|------------
# 03 13 23 | 43 53 63 73
# 04 14 24 | 44 54 64 74
# 05 15 25 | 45 55 65 75
# 06 16 26 | 46 56 66 76
# 07 17 27 | 47 57 67 77
#
# The bottom right of the (22) LED was at the center of the optical axis. The lines here indicate approximately the position of the x 
# and y-axis. So the origin of the xy plane can be taken to be along the center of the 3rd row and along the tangent to the circular 
# LEDs of the 2nd column. This is precisely (26.44, 20.82) mm from the origin of the 8x8 array as given at 
# http://www.ebay.in/itm/8x8-RGB-LED-Matrix-Common-Anode-Diffused-Arduino-Full-Colour-RGB-Color-60mm-/151453142648?aff_source=vizury
# 
# Each LED's center is 7.62mm away from the next
# The distance between the LED array and the transparency is 78 mm.
#   
# The camera used for imaging was a Jenoptik ProgRes C3, with 416x308 pixel resolution of images taken. Pixel dimensions are 3.45 micron^2 
# The sensor size is 7.58 mm x 6.54 mm, and the max resolution attainable is 2080 x 1542 pixels 
#   
## we assume that the authors are completely correct in their assumption that the shift in the fourier domain shall be
# precisely (kx, ky), where these correpond to the wavevectors of each LED source.
# The wavevector has ampitude equal to the wavenumber in each cartesian axis
# The wavevector (kx, ky, kz) has a direction given by a unit vector from the light source to the point of illumination on the sample - this
# will be taken as the origin in 3D cartesian coordinates in this frame of reference.
#
# The wavevector for the LED at (a,b,-l) is (-l is fixed since the LED array lies in the z=-l plane
# (a, b, -l)*(2*pi/{lambda*sqrt(a^2 + b^2 + l^2)}). 
#

###### importing required modules
import numpy, pylab, Image, scipy.misc, matplotlib.cm as cm, os

###### UNIVERSAL DEFINITIONS
## Experimental setup constants
NA = 0.06		# numerical aperture of objective
d = 7.62		# distance between LED centers in mm
l = 78			# distance from transparency to the LED array in mm
x = 3.58		# distance in x-axis from top left of LED array to first LED's center
y = 3.58		# distance in y-axis from top left of LED array to first LED's center
origin = [26.44, 20.82]	# the origin w.r.t. the top left of the LED array (as seen from +ve z-axis
lmbda = 623		# dominant wavelength of the monochromatic light source, in nm
n = 8			# single dimension of the (square) LED array.

## mathematical and physical constants
pi = 3.141592		# apple pie

## System constants
reading_folder = "./images/"	# the folder where the files of the name given above lie..
saving_folder = "./images/fpm/"	# the folder where we'll save the various iterations of the images and their FTs to
filetype = ".jpg"
filename = "00"		# the chosen file to be the upsampled guess image, or starting point 
number_iterations = 1	# no of times we will iterate the FPM reconstruction algo

## definitions which derive from these universal definitions..
led_array = numpy.empty([n,n], dtype=object)	# 'object' because we will be making a 2d array of tuples
wave_number = 2*pi/lmbda
upsampling_scaling_factor = 2		# the scaling factor by which we will enhance the resolution of the image

### FUNCTION DEFINITIONS
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

## Next we have a function that replaces the sqrt of Intensity of the complex image expressed in the form sqrt(I)*exp(j*Phase) 
# and returns an image back again. Since this comes from the phase retreival algorithm developed by Fienup, we will name it after him.
def fienup_intensity_replace(source_image, replacement_intensity_image):
  shape = source_image.shape
  target_image = numpy.zeros(source_image.shape)	# the target image which shall be returned
  # Now remember that the source image is an mxn complex image. We will cycle through each pixel
  for m in range(0, shape[0]):
    for n in range(0, shape[1]):
      current_complex_pixel = source_image[i][j]
      current_complex_pixel_intensity = numpy.abs(current_complex_pixel)	# find the sqrt(a2 + b2) of a + ib
      target_image[i][j] = numpy.abs(replacement_intensity_image)*current_complex_pixel/current_complex_pixel_intensity
  
  return target_image


#### So we'll start by upsampling the one we know is the 'central' one, i.e. who's FT circular mask is in the center
####

print("STEP 1: Starting with guess image...")
central_image = Image.open(reading_folder + filename + filetype).convert("L")
ncentral = numpy.array(central_image)

print("upsampling the guess image...")

# now the actual upsampling..
upsampled = scipy.misc.imresize(ncentral, (upsampling_scaling_factor*ncentral.shape[0], upsampling_scaling_factor*ncentral.shape[1]))
upsampled_guess_image = Image.fromarray(upsampled)
# pylab.figure(); pylab.imshow(upsampled_guess_image, cmap=cm.Greys_r); pylab.show()

# and we save it
upsampled_guess_image.save(saving_folder + 'starting_guess' + filetype)

# we find its fourier transform and keep it handy
starting_ft = 20*numpy.log(numpy.abs(numpy.fft.fftshift(numpy.fft.fft2(up_channel))))
starting_ft_image = Image.fromarray(starting_ft.astype(numpy.uint8))
starting_ft_image.save(saving_folder + 'starting_guess_ft' + filetype)

print("FT of the upsampled image calculated and saved. Now begins the stitching process.")

#### HERE IS THE MAIN MASALA
## Now the iterative stitching part. THis will relate a displacement of (x,y) in the LED aray plane to a shift (kx, ky) in the fourier domain.
# The mask for this shift will be a circle in fourier space with a radius of 2*pi*NA/lambda 
# first we have a for loop which loops over all the LEDs in the array

for iterations in range(0, number_iterations):
  for i in range(0,n):	# x-direction
    for j in range(0,n):	# y-direction
      # start by checking whether a particular illumination (LED) file exists, if not move on
      print("Checking if " + str(i) + str(j) + " exists...")
      if (os.path.isfile(reading_folder + str(i) + str(j) + filetype):
        # Now we can move on
        print("..exists. processing...")
        # We find the (a,b) in mm, position of the present LED in the xy plane, absolute units.
        a = round(x + d*i - origin[0], 2 
        b = round(y + d*j - origin[1], 2
        k_denominator = math.sqrt(a**2 + b**2 + l**2)
        wave_vector = [a*wave_number/k_denominator, b*wave_number/k_denominator]
        # TODO: scale wave_number to same units as the FT

        print("calculated k-vector. Now will extract the FT of upsampled at (kx, ky) with pupil NA*k")
        system_ft = starting_ft		# make a copy of the upsampled FT
        k_pupil = circular_mask(starting_ft.shape, [wave_vector], wave_number*NA)
        system_ft[~k_pupil] = 0		# remove everything in the FT except in the pupil area
        
        # Now we convert this to an image.
        
      else:
       print("No file found. moving to next iteration...")
  # next iteration

# At this point we are done with the FPM retreival.

