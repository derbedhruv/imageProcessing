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
# Data was taken on 03-march-2015 
# The illumination of the system was done as follows: (the row-column numbers are exact)
# 
# 00 10 20 30 | 50 60 70 
# 01 11 21 31 | 51 61 71
# 02 12 22 32 | 52 62 72
# 03 13 23 33 | 53 63 73
# 04 14 24 34 | 54 64 74
# 05 15 25 35 | 55 65 75
# 06 16 26 36 | 56 66 76
# 07 17 27 37 | 57 67 77
#
# The 4,4 was taken to be the center of the optical axis (the system was manipulated in such a way). The distance between centers of 
# each LED was 4mm, and the distance between the outermost LEDs and the edge of the matrix was 2mm.  Hence the optical axis passes through
# the point (14, 18) from the top left (The orientation of the LED matrix was such that (0,0) was on the top right and (0,7) was on the 
# bottom left. 
#  
# The distance between the LED array and the transparency is 83 mm.
#   
# The camera used for imaging was a Jenoptik ProgRes C3, with a 2080x1642 pixel resolution of images taken. Pixel dimensions are 
# 3.45x3.45 micron. The magnification factor on the microscope is 2x, so all dimensions would be scaled down by that factor.  
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
d = 4.			# distance between LED centers in mm
l = 83.			# distance from transparency to the LED array in mm
x = 2.			# distance in x-axis from top left of LED array to first LED's center (mm)
y = 2.			# distance in y-axis from top left of LED array to first LED's center (mm)
origin = [14., 18.]	# the origin w.r.t. the top left of the LED array (as seen from +ve z-axis
lmbda = 0.623		# dominant wavelength of the monochromatic light source, in microns
n = 8			# single dimension of the (square) LED array.
pixel_size = 3.45	# pixel dimensions in microns
magnification = 2	# image magnification w.r.t. object by the objective

## mathematical and physical constants
pi = 3.141592		# apple pie

## System constants
reading_folder = "./20150303_fpm/"	# the folder where the files of the name given above lie..
saving_folder = "./images/fpm/"	# the folder where we'll save the various iterations of the images and their FTs to
filetype = ".jpg"
filename = "44"		# the chosen file to be the upsampled guess image, or starting point 
number_iterations = 1	# no of times we will iterate the FPM reconstruction algo

## definitions which derive from these universal definitions..
led_array = numpy.empty([n,n], dtype=object)	# 'object' because we will be making a 2d array of tuples
wave_number = 2*pi/lmbda			# in micron-1
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
  target_image = numpy.zeros(source_image.shape, dtype=source_image.dtype)	# the target image which shall be returned
  # Now remember that the source image is an mxn complex image. We will do this the numpy way. the faster way.
  # i.e. create three individual 2d numpy arrays and multiple them
  replacement_intensity = numpy.abs(replacement_intensity_image)
  source_intensity = numpy.abs(source_image)

  # now the multiplication
  target_image = numpy.sqrt(replacement_intensity*source_image/source_intensity)

  return target_image


#### So we'll start by upsampling the one we know is the 'central' one, i.e. who's FT circular mask is in the center
####

print("STEP 1: Starting with guess image...")
central_image = Image.open(reading_folder + filename + filetype).convert("L")
ncentral = numpy.array(central_image)

## from this image we find the conversion factor of spatial frequency into pixels..
sfrq_to_px = upsampling_scaling_factor*max(ncentral.shape)/(pixel_size*magnification)

print("upsampling the guess image...")

# now the actual upsampling..
upsampled_size = [upsampling_scaling_factor*ncentral.shape[0], upsampling_scaling_factor*ncentral.shape[1]]
upsampled = scipy.misc.imresize(ncentral, upsampled_size)
upsampled_guess_image = Image.fromarray(upsampled)
# pylab.figure(); pylab.imshow(upsampled_guess_image, cmap=cm.Greys_r); pylab.show()

# and we save it
upsampled_guess_image.save(saving_folder + 'starting_guess' + filetype)

# we find its fourier transform and keep it handy
# to prevent a memory error from happening, this will be done in seperate steps...
starting_ft = numpy.fft.fft2(upsampled_guess_image)
starting_ft = numpy.fft.fftshift(starting_ft)
starting_psd = 20*numpy.log(numpy.abs(starting_ft))
starting_ft_image = Image.fromarray(starting_psd.astype(numpy.uint8))
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
      if (os.path.isfile(reading_folder + "/" +  str(i) + str(j) + filetype)):
        # Now we can move on
        print("..exists. processing...")
        # We find the (a,b) in mm, position of the present LED in the xy plane, absolute units.
        a = round(x + d*i - origin[0], 2)
        b = round(y + d*j - origin[1], 2)
        k_denominator = numpy.sqrt(a**2 + b**2 + l**2)

        # now the most important part - we calculate the wavevector (kx, ky) and scale it to the units of pixels in the fourier domain
        # explanation:
        # the image is flipped in both axes w.r.t. the object, so the wavenumber will have to be made -ve in both dimensions
        # then we use the scaling factor which was calculated earlier.
        wave_vector = [b*(wave_number/k_denominator)*sfrq_to_px, -a*(wave_number/k_denominator)*sfrq_to_px]
        k_shift = [int(wave_vector[0] + starting_ft.shape[0]/2), int(wave_vector[1] + starting_ft.shape[1]/2)]
        print(k_shift)

        print("calculated k-vector. Now will extract the FT of upsampled at (kx, ky) with pupil NA*k")
        system_ft = numpy.copy(starting_ft)		# make a copy of the upsampled FT
        k_pupil = circular_mask(starting_ft.shape, k_shift, sfrq_to_px*wave_number*NA)
        center_pupil = circular_mask(starting_ft.shape, [starting_ft.shape[0]/2, starting_ft.shape[1]/2], sfrq_to_px*wave_number*NA)

        # now we remove a circular section of the spectrum and use that to be the center of the FT of an image
        system_ft[:] = 0+0j
        system_ft[center_pupil] = starting_ft[k_pupil]
        
        # Now we convert this to an image.
        generated_lowres_image = numpy.fft.fftshift(system_ft)
        generated_lowres_image = numpy.fft.ifft2(generated_lowres_image)
        print(numpy.average(generated_lowres_image))
        
        # we then read in the corresponding measured image, and upsample it
        measured_lowres_image = numpy.array(Image.open(reading_folder + str(i) + str(j) + filetype).convert("L"))
        measured_highres_image = scipy.misc.imresize(measured_lowres_image, upsampled_size)
        
        # going to replace the sqrt(intensity) of the generated image with the intensity of this upsampled measured image
        replaced_intensity_image = fienup_intensity_replace(generated_lowres_image, measured_highres_image)

        # now we simply have to take its FFT and replace the corresponding section of the FFT in the original FFT where we chopped from
        replaced_intensity_ft = numpy.fft.fftshift(numpy.fft.fft2(replaced_intensity_image))
        starting_ft[k_pupil] = replaced_intensity_ft[center_pupil]

        # and this round is done, now go on to the other rounds of replacement
        # but we will show the image and ft (for debugging)
        # current_ft = numpy.log(numpy.abs(starting_ft))
        # current_ft = Image.fromarray(current_ft.astype(numpy.uint8))
        # pylab.figure()
        # pylab.imshow(current_ft, cmap=cm.Greys_r)
        
        current_image = numpy.fft.fftshift(starting_ft)
        current_image = numpy.fft.ifft2(current_image)
        
        current_image = Image.fromarray(current_image.astype(numpy.uint8))
        current_image.save(saving_folder + "fpm_image" + filetype)
        # pylab.figure()
        # pylab.imshow(current_image, cmap=cm.Greys_r)

        # At this point we are done with the FPM retreival.
        # pylab.show()
      else:
       print("No file found. moving to next iteration...")
  # iteration done.
  print("ITERATION OVER. will print out image and FT")
  current_ft = 20*numpy.log(numpy.abs(starting_ft))
  current_ft = Image.fromarray(current_ft.astype(numpy.uint8))
  pylab.figure()
  pylab.imshow(current_ft, cmap=cm.Greys_r)
  
  current_image = numpy.fft.ifft2(numpy.fft.fftshift(starting_ft))

  current_image = Image.fromarray(current_image.astype(numpy.uint8))
  current_image.save(saving_folder + "fpm_image" + filetype)
  pylab.figure()
  pylab.imshow(current_image, cmap=cm.Greys_r)

# At this point we are done with the FPM retreival.
pylab.show()

