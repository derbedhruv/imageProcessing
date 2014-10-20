% 19-OCT-2014
% first I'm going to start by reading in an image and converting it to greyscale
% I'll use imread()

img = imread('pic.jpg');        % read in the pic into an array

% convert to greyscale
gimg = rgb2gray(img);

% next we display the two images side by side. ref: http://www.mathworks.in/help/images/displaying-images-using-the-imshow-function.html
subplot(2,2,1), imshow(img,'Border','tight');   % read above link to find out about subplots and even imshow()
subplot(2,2,2), imshow(gimg,'Border','tight');

% next we find the fourier transform of the greyscaled image...
F = fft2(gimg,512,512);
F = fftshift(F);            % shift the center
subplot(2,2,[3 4]), imshow(abs(F),[0,100]); colorbar          % asymmetrical arrangement of subplots is done this way
