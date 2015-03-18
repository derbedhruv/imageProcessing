# This will enable us to visualize the histograms of the images which have been acquired, and, if not good, to stretch them to max contrast
import Image, os, sys
import numpy 
import matplotlib.pyplot as plt

# Next we include the histogram equalization function which is presnt in the folder above..
sys.path.append('../')
import histeq
sys.path.append('./')

for i in range(0,7):
  for j in range(0,7):
    filename = str(i) + str(j) + '.jpg'
    if(os.path.isfile('./' + filename)):
      im = numpy.array(Image.open(filename).convert('L'))
      
      im, cdf = histeq.histeq(im)
      im = Image.fromarray(im.astype(numpy.uint8))
      im.save('histeq/' + str(i) + str(j) + '.jpg')

      # plt.hist(im.ravel(),256,[0,256],histtype='step')

plt.show()
