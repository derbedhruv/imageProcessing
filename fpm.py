# THis file shall stitch together the small images in the fourier domain and produce a higher res image
# Remember the images are such (2D fourier domain) ..
# 
# 	02  12  22
# 	01  11  21
#	00  10  20
#
# Where each step indicates a step in 50 in the fourier domain. Remember that 11 is the actual (0,0).
import numpy, pylab, Image, scipy.misc

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
upsampled_guess_image.save(folder + 'upsampled' + filetype)

# pylab.show()

#### 
