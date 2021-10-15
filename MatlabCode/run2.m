clear ALL
close ALL
clear

format short
load("stereoParams.mat");

%I1 = imread('1.png');
%I2 = imread('2.png');

%I1 = undistortImage(I1,stereoParams.CameraParameters1);
%I2 = undistortImage(I2,stereoParams.CameraParameters2);
%class(I1)

%imwrite(I1, 'undistort1.png');
%imwrite(I2, 'undistort2.png');


%usb pixel point
usb1 = [29, 335];
usb2 = [154, 362];
point3d_usb = triangulate(usb1, usb2, stereoParams)
distance_usb = norm(point3d_usb); %in mm

%usb pixel point
usb1 = [166, 263];
usb2 = [247, 289];
point3d_usb = triangulate(usb1, usb2, stereoParams)
distance_usb = norm(point3d_usb); %in mm

%usb pixel point
usb1 = [307, 179];
usb2 = [349, 189];
point3d_usb = triangulate(usb1, usb2, stereoParams)
distance_usb = norm(point3d_usb); %in mm

%usb pixel point
usb1 = [466, 224];
usb2 = [558, 210];
point3d_usb = triangulate(usb1, usb2, stereoParams)
distance_usb = norm(point3d_usb); %in mm



