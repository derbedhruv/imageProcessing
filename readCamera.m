% copied from Sujeath's code on 19-OCT-2014
% now tracked by git on my github
% This code can successfully take a stream from a webcam attached to a computer (windows) and display to screen

vid = videoinput('winvideo', 1,'YUY2_320x240');          % Video Parameters
set(vid,'ReturnedColorSpace','grayscale');      % acquire in greyscale
triggerconfig(vid, 'manual');					% the magic sauce that tells matlab that the triggering for 'getsnapshot' will be manual, which helps us speed it up

start(vid);                                     % start acquiring from imaqwindow
gcf = figure;                                   % figure object

set(gcf,'CloseRequestFcn',@my_closefcn)			% setting the close request . More here: http://www.mathworks.in/matlabcentral/newsreader/view_thread/255448
hold on;										% image will persist. to close from command line can use delete(gcf) and then delete(vid) - which is basically deleting the variables
closeflag = 1;                                  % for now this doesn't really do anythng, but will just keep the while loop going forever

while(closeflag)                                % infinite loop
    imshow(getsnapshot(vid));                   % display the image
    pause(0.001);                               % much less than 30 fps
end% Preview