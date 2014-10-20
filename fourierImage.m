% 19-OCT-2014
% first I'm going to start by reading in an image and converting it to greyscale
% I'll use imread()

img = imread('pic.jpg');        % read in the pic into an array
gimg = rgb2gray(img);

% next we display the two images side by side. ref: http://www.mathworks.in/help/images/displaying-images-using-the-imshow-function.html
subplot(1,2,1), imshow(img,'Border','tight');   % read above link to find out about subplots and even imshow()
subplot(1,2,2), imshow(gimg,'Border','tight');