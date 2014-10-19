% copied from Sujeath's code on 19-OCT-2014
% now tracked by git on my github
% This code can successfully take a stream from a webcam attached to a computer (windows) and display to screen

vid = videoinput('winvideo', 1,'YUY2_320x240');          % Video Parameters
set(vid,'ReturnedColorSpace','grayscale');      % acquire in greyscale
triggerconfig(vid, 'manual');					% the magic sauce that tells matlab that the triggering for 'getsnapshot' will be manual, which helps us speed it up

start(vid);
gcf = figure;

set(gcf,'CloseRequestFcn',@my_closefcn)			% setting the close request 
hold on;										% image will persist. to close from command line can use delete(gcf)
closeflag = 1;

while(closeflag)
    imshow(getsnapshot(vid));
    pause(0.01);
end% Preview