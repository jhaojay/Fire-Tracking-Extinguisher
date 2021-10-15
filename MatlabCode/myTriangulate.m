function camWorldCoordinates = myTriangulate(cam1Pixels_x, cam1Pixels_y, cam2Pixels_x, cam2Pixels_y)
    load("stereoParams.mat");
    cam1Pixels = [cam1Pixels_x, cam1Pixels_y];
    cam2Pixels = [cam2Pixels_x, cam2Pixels_y];
    camWorldCoordinates = triangulate(cam1Pixels, cam2Pixels, stereoParams);
end