# this is me experimenting wiht image processing in python using openCV

import cv2		# and this it was imported
import numpy as np
img = cv2.imread('C:\Users\croma\Dropbox\cameraculture\image_processing\dj.jpg')	# adding a 0 as second attribute means grayscale

# print info about the image
print img.size
print img.dtype
# print img
print img[0,0]			# how does this work? img[x,y,colour coordinate]. (x,y) refers to the column and row point

# process the image
img[:,:,2] = 0			# the third coordinate here gives the B,G,R respectively for 0,1,2 as the value

# show the image

cv2.imshow('image',img[0:200, 0:450])
cv2.waitKey(0)
cv2.destroyAllWindows()
