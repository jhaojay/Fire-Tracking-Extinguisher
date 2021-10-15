function a = undistortImgs(path, img_name1, img_name2)
    a = 1;
    load("stereoParams.mat");
    userpath (path);
    
    I1 = imread(img_name1);
    I2 = imread(img_name2);
    
    I1 = undistortImage(I1,stereoParams.CameraParameters1);
    I2 = undistortImage(I2,stereoParams.CameraParameters2);
    
    imwrite(I1, path + "\undistorted_" + img_name1);
    imwrite(I2, path + "\undistorted_" + img_name2);
end
    