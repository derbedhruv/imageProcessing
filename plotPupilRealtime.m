%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 																 
%    Aim : Pupil detection and diameter plot							 
%    Authors : Dhruv Joshi											 
%    Acknowledgements : Sujeath Pareddy, Sandeep Konam
%    Organization : Srujana - Center for Innovation, LVEPI						 	 
%																 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Approach :: Extracting frames -> Thresholding the frame at hand  -> cropping out excess -> Circle Detection(Pupil Approximation) -> Radius measurement -> Plotting the graph
% to be able to see the two feeds (greyscale and thresholded) simultaneously, uncomment the subplot part.

close all;
clear all;
clc;

vid = videoinput('winvideo', 1,'YUY2_320x240');          % Video Parameters
set(vid,'ReturnedColorSpace','grayscale');      % acquire in greyscale
triggerconfig(vid, 'manual');					% manual trigger, increase speed

start(vid);                                     % start acquiring from imaqwindow
gcf = figure;                                   % figure

set(gcf,'CloseRequestFcn',@my_closefcn)			% this is incomplete
hold on;										% image will persist
closeflag = 1;                                  % for now this doesn't really do anythng

while(closeflag)                                % infinite loop
    %% first we acquire the feed and crop out unrequired parts to speed it all up
    acquired_snapshot = getsnapshot(vid);       % acquire single image from feed
    cropped_snapshot = imcrop(acquired_snapshot,[85 50 140 112]);   % crop it out so that you can see just the center ref: http://www.mathworks.in/help/images/ref/imcrop.html
    % subplot(1,2,1), imshow(cropped_snapshot);  % normal camera (greyscale)
    
    %% Then we threshold it to some value of threshold to be able to get the pupil out
    thresholded_image = im2bw(cropped_snapshot,0.37);   % threshold karo... this value has been obtained after playing around
    %subplot(1,2,2), 
    imshow(thresholded_image);  % display the image
        
    %% next we extract circles from this baby...and plot them if they are found
    [centers, radii] = imfindcircles(thresholded_image,[10 17], 'ObjectPolarity','dark','Sensitivity',0.91); 
    if ~isempty(centers)                        % plot only if circle is detected.. ~ is logical not. simple error handling for viscircles
      %subplot(1,2,2), 
      viscircles(centers, radii,'EdgeColor','b');
    end
    
    pause(0.001);                               % much less than 30 fps. wihtout this it doesn't seem to work
end% Preview