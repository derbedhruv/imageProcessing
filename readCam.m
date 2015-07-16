% copied from Sujeath's code on 19-OCT-2014
% now tracked by git on my github
% This code can successfully take a stream from a webcam attached to a computer (windows) and display to screen

%{
vid = videoinput('winvideo', 1,'YUY2_640x480');          % Video Parameters
set(vid,'ReturnedColorSpace','rgb');      % acquire in greyscale
% set(vid,'FocusMode','manual');                  % from http://www.edaboard.com/thread132976-4.html
triggerconfig(vid, 'manual');					% the magic sauce that tells matlab that the triggering for 'getsnapshot' will be manual, which helps us speed it up

start(vid);                                     % start acquiring from imaqwindow
gcf = figure;                                   % figure object

set(gcf,'CloseRequestFcn',@my_closefcn)			% setting the close request . More here: http://www.mathworks.in/matlabcentral/newsreader/view_thread/255448
set(vid, 'Focus',10);
hold on;										% image will persist. to close from command line can use delete(gcf) and then delete(vid) - which is basically deleting the variables
closeflag = 1;                                  % for now this doesn't really do anythng, but will just keep the while loop going forever

while(closeflag)                                % infinite loop
    imag = getsnapshot(vid);
    imshow(imag(:,:,1));                   % display the image
    pause(0.001);                               % much less than 30 fps
end% Preview

%}
%% This is an even better way to do the same thing ... and add post processing.
%% Fisrt you need to install the 'webcam' MATLAB support packgage. Use the following command..
% hwconnectinstaller.launchInstaller('SupportPackageFor','USB Webcams','StartAtStep','SelectPackage');

%% Next we open up a new webcam object instance..
wcam = webcam()  % open up the externally connected webcam if any, and display its properties

%% Next we set camera properties based on what's needed
set(wcam,'FocusMode','manual');
set(wcam, 'Focus', 40); % max value

%% display the live feed from the camera.
% preview(wcam);

%% process the live feed from the camera by taking images from the feed
for idx = 1:100
    rgb = snapshot(wcam);       % get a snapshot
    
    % g = rgb2gray(rgb);          % grayscale
    g = rgb(:,:,2);
    
    i = histeq(g);        % adaptive histogram equalization
    
    % i = edge(gh, 'canny');
    
    % display karo
    imshow(i,[])
    hold on;
end

clear all;