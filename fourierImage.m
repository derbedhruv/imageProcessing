% 19-OCT-2014
% first I'm going to start by reading in an image and converting it to greyscale
% I'll use imread()

% 24-OCT-2014
% Trying out standard images to be able to see how the fft changes

% 04-JAN-2015
% Following simple advice given on http://stackoverflow.com/questions/13549186/how-to-plot-a-2d-fft-in-matlab

ford = 256;     % fourier order
dord = 1024;    % display order

img = imread('fpm1.png');        % read in an FPM-taken pic into the array

% convert to greyscale
gimg = rgb2gray(img);

% take the fft2
f = fft2(gimg);

% Then we do an "fftshift" to center the fft ... need to do this with and without and see the diff in reality
f = fftshift(f);

% Next we take the magnitude of the fft
f = abs(f);

% These are usually really small, we will take the log
f = log(f + 1)		% 1 is added to prevent log(0) from happening

% Next we normalize between 0 and 1
f = mat2gray(f)

% Now we're going to display it
imshow(f)