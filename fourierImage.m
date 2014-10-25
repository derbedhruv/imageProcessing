% 19-OCT-2014
% first I'm going to start by reading in an image and converting it to greyscale
% I'll use imread()

% 24-OCT-2014
% Trying out standard images to be able to see how the fft changes
ford = 256;     % fourier order
dord = 1024;    % display order

img = imread('test.jpg');        % read in the pic into an array

% convert to greyscale
gimg = rgb2gray(img);

% next we display the two images side by side. ref: http://www.mathworks.in/help/images/displaying-images-using-the-imshow-function.html
% subplot(3,2, 1), imshow(img,'Border','tight');   % read above link to find out about subplots and even imshow()
% subplot(1,2,1), imshow(gimg,'Border','tight');

% next we find the fourier transform of the greyscaled image...http://biocomp.cnb.csic.es/~coss/Docencia/ImageProcessing/Tutorial/
F = fft2(gimg, ford, ford);
F = fftshift(F);            % shift the center
% subplot(3,2,[3 6]), imshow(abs(F),[0,dord]); colorbar          % asymmetrical arrangement of subplots is done this way http://matlab.izmiran.ru/help/techdoc/ref/subplot.html
% subplot(1,2,2), 
imshow(abs(F),[0,dord]); colorbar 
