import matplotlib.cm as cm, scipy.misc, numpy, Image, pylab

scale = 10

im = Image.open("../images/44.jpg").convert("L")

imar = numpy.array(im)

print(scale*imar.shape[0], scale*imar.shape[1])
upsampled = scipy.misc.imresize(im, (scale*imar.shape[0], scale*imar.shape[1]))

ft = numpy.fft.fft2(upsampled)

# ft_image = Image.fromarray(ft.astype(numpy.uint8))
# ft_image.save("fft.png")

# Now we're going to chop out a section of the FT and see what it looks like
def circular_mask(shape,centre,radius):
    """
    Return a boolean mask for a circular sector. The start/stop angles in  
    `angle_range` should be given in clockwise order.
    """
    angle_range = [0,360]
    x,y = numpy.ogrid[:shape[0],:shape[1]]
    cx,cy = centre
    tmin,tmax = numpy.deg2rad(angle_range)
    if tmax < tmin:
            tmax += 2*numpy.pi
    r2 = (x-cx)*(x-cx) + (y-cy)*(y-cy)
    theta = numpy.arctan2(x-cx,y-cy) - tmin
    theta %= (2*numpy.pi)
    circmask = r2 <= radius*radius
    anglemask = theta <= (tmax-tmin)
    return circmask*anglemask

ft_mask = circular_mask(ft.shape, [ft.shape[0]/2 + 200, ft.shape[1]/2], 200)
# print(ft_mask.shape)

ft = numpy.fft.fftshift(ft)
ft[~ft_mask] = 0

chopped_ft = 20*numpy.log(numpy.abs(ft) + 1)
# print(chopped_ft.shape)

chopped_ifft = numpy.fft.ifft2(numpy.fft.fftshift(ft))
print(chopped_ifft.shape)

chopped_image = Image.fromarray(chopped_ifft.astype(numpy.uint8))
chopped_image = scipy.misc.imresize(chopped_image, (imar.shape[0], imar.shape[1]))

pylab.figure()
pylab.imshow(chopped_ft, cmap = cm.Greys_r)

pylab.figure()
pylab.imshow(chopped_image, cmap = cm.Greys_r)

pylab.show()
