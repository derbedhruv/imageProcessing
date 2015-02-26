import matplotlib.cm as cm, scipy.misc, numpy, Image, pylab

scale = 10

im = Image.open("../images/44.jpg").convert("L")

imar = numpy.array(im)

print(scale*imar.shape[0], scale*imar.shape[1])
upsampled = scipy.misc.imresize(im, (scale*imar.shape[0], scale*imar.shape[1]))

ft = 20*numpy.log(numpy.abs(numpy.fft.fftshift(numpy.fft.fft2(upsampled))))

ft_image = Image.fromarray(ft.astype(numpy.uint8))
# ft_image.save("fft.png")

pylab.figure()
pylab.imshow(ft, cmap = cm.Greys_r)
pylab.show()
