# This will enable us to visualize the histograms of the images which have been acquired, and, if not good, to stretch them to max contrast
import Image, os
from numpy import *
import matplotlib.pyplot as plt

for i in range(0,7):
  for j in range(0,7):
    filename = str(i) + str(j) + '.jpg'
    if(os.path.isfile('./' + filename)):
      im = array(Image.open(filename).convert('L'))
      plt.hist(im.ravel(),256,[0,256],histtype='step')

plt.show()
