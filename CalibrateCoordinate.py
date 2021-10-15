import cv2
import matlab.engine
import os
import numpy as np
import shutil
import sys

import getMyWorldCoordinates
import getTopPixel


#================ find top pixels
#
img_path = os.getcwd() + r"\CoordinateCalibrationImages"
top_pixels_1 = []
top_pixels_2 = []
print("Please click on the top points of the chess pieces...")
for i in range(4):
    print("\nRow {}".format(i))
    image_1 = cv2.imread(img_path + r'\undistorted_cam_1.{}.png'.format(i))
    image_2 = cv2.imread(img_path + r'\undistorted_cam_2.{}.png'.format(i))
    row_1, row_2 = getTopPixel.getTopPixel(image_1, image_2)
    top_pixels_1.append(row_1)
    top_pixels_2.append(row_2)
print("\nArrays recorded.\n")

#============== find camera's world coordinates
#
print("Using MatLab to get camera's world coordinates...\n")
eng = matlab.engine.start_matlab()
matlab_code_path = os.getcwd() + '\MatlabCode'
eng.cd(matlab_code_path)

try:
    ml_world_coordinate_cam = []
    for i in range(len(top_pixels_1)):
        for j in range(len(top_pixels_1[i])):
            cam1Pixels_x = top_pixels_1[i][j][0]
            cam1Pixels_y = top_pixels_1[i][j][1]
            cam2Pixels_x = top_pixels_2[i][j][0]
            cam2Pixels_y = top_pixels_2[i][j][1]
            coor = eng.myTriangulate(cam1Pixels_x,cam1Pixels_y, cam2Pixels_x, cam2Pixels_y)
            ml_world_coordinate_cam.append(coor)
    eng.quit()
    print("Camera's world coordinates obtained\n")
except:
    print("The arrays don't look good. You may want to re-try.")
    sys.exit()

# process MatLab results
world_coordinate_cam = []
coordinate = []
for i in range(len(ml_world_coordinate_cam)):
    for c in ml_world_coordinate_cam[i][0]:
        coordinate.append(c)
    world_coordinate_cam.append(coordinate)
    coordinate = []
world_coordinate_cam = np.asarray(world_coordinate_cam)


#================ get my world coordinates using SVD
#
print("Using SVD to get R and d...\n")
P = 45.2
R = 41
B = 64.9
Q = 74.5
K = 96.2

preset_my_world_coordinates = np.asarray([[30, 20, P], [70, 80, B], [40, 130, P], [60, 170, R],
                                          [90, 10, B], [100, 90, Q], [110, 130, R], [80, 190, P],
                                          [150, 40, K], [170, 90, P], [130, 130, R], [140, 180, B],
                                          [230, 30, R], [220, 70, B], [210, 110, K], [200, 170, Q]])

# preset_my_world_coordinates = np.asarray([[30, 20, P],
#                                           [100, 90, Q],
#                                           [130, 130, R],
#                                           [200, 170, Q]])

R, d = getMyWorldCoordinates.getMyWorldCoordinates(world_coordinate_cam, preset_my_world_coordinates)

x_test = [-140.9235,  -82.4707,  443.0979]
print("test:\n", np.matmul(R, x_test) + d, "\n")

print("R is:\n", R)
print("d is:\n", d)

#=============== testing
#

