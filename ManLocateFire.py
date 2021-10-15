import serial
import time
import cv2
import matlab.engine
import os
import numpy as np
from termcolor import colored

import getTopPixel



R = np.asarray( [[ 0.06396712,  0.65312681, -0.75454197],
 [ 0.99776758, -0.02732128,  0.0609377 ],
 [ 0.019185,   -0.75675552, -0.65341642]])

d = np.asarray([404.55821559,  69.31332313, 250.10474557])

img_path = os.getcwd() + r"\CoordinateCalibrationImages"

eng = matlab.engine.start_matlab()
matlab_code_path = os.getcwd() + r'\MatlabCode'
eng.cd(matlab_code_path)

cam_1 = cv2.VideoCapture(1)
cam_2 = cv2.VideoCapture(0)

arduinoData = serial.Serial('COM3', 9600)
time.sleep(2)  # Let Arduino some time to reset

while True:
    ret_1, frame_1 = cam_1.read()
    ret_2, frame_2 = cam_2.read()

    if not ret_1:
        print("failed to grab frame")
        break
    cv2.imshow("cam_1", cv2.flip(frame_1, -1))

    if not ret_2:
        print("failed to grab frame")
        break
    cv2.imshow("cam_2", frame_2)

    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        cam_1.release()
        cam_2.release()
        cv2.destroyAllWindows()
        break
    elif k % 256 == 32:
        # SPACE pressed
        img_name_1 = img_path + r"\testing_cam_1.png"
        cv2.imwrite(img_name_1, cv2.flip(frame_1, -1))
        print("{} written!".format(img_name_1))

        img_name_2 = img_path + r"\testing_cam_2.png"
        cv2.imwrite(img_name_2, frame_2)
        print("{} written!".format(img_name_2))

        print("\nGenerating undistorted images using MatLab...")
        img_path = os.getcwd() + r'\CoordinateCalibrationImages'
        eng.undistortImgs(img_path, "testing_cam_1.png", "testing_cam_2.png")
        print("Undistorted images generated.\n")

        print("\nObtaining top pixel... Please click on the points on the images...")
        image_1 = cv2.imread(img_path + r'\undistorted_testing_cam_1.png')
        image_2 = cv2.imread(img_path + r'\undistorted_testing_cam_2.png')
        top_pixels_1, top_pixels_2 = getTopPixel.getTopPixel(image_1, image_2)

        cam1Pixels_x = top_pixels_1[0][0]
        cam1Pixels_y = top_pixels_1[0][1]
        cam2Pixels_x = top_pixels_2[0][0]
        cam2Pixels_y = top_pixels_2[0][1]
        coor = eng.myTriangulate(cam1Pixels_x, cam1Pixels_y, cam2Pixels_x, cam2Pixels_y)

        world_coor = np.asarray(coor[0])
        world_coor = np.matmul(R, world_coor) + d
        round_world_coor = [int(round(world_coor[0])), int(round(world_coor[1])), int(round(world_coor[2]))]
        print("\nFire Location: ", colored(round_world_coor, 'red') , "\n")

        # decoding coordinates to send to Arduino
        command = ""
        for i in round_world_coor:
            if i < 0:
                i = 0
            if i/10 < 1:
                command = command + "00" + str(i)
            elif i/10 < 10:
                command = command + "0" + str(i)
            else:
                command = command + str(i)

        arduinoData.write(command.encode())

        print("New Round:")
        print("Please hit Space Bar to take pictures or ESC to quit.")

        cv2.destroyAllWindows()

eng.quit()