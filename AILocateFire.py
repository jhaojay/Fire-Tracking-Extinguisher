import serial
import cv2
import time
import os
import shutil
import numpy as np
import matlab.engine
from termcolor import colored



# define the countdown func.
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
        print(t)

def empty_a_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# rotation matrix and translation matrix from CoordinateCalibration.py
R = np.asarray( [[ 0.06396712,  0.65312681, -0.75454197],
 [ 0.99776758, -0.02732128,  0.0609377 ],
 [ 0.019185,   -0.75675552, -0.65341642]])

d = np.asarray([404.55821559,  69.31332313, 250.10474557])


print("Pre-loading")
arduinoData = serial.Serial('COM3', 9600)
time.sleep(2)  # Let Arduino some time to reset

from imageai.Detection.Custom import CustomObjectDetection
execution_path = os.getcwd()
empty_a_folder(execution_path + r"\monitoring")
eng = matlab.engine.start_matlab()
matlab_code_path = os.getcwd() + r'\MatlabCode'
eng.cd(matlab_code_path)

# pre-loading fire_net
detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(detection_model_path=os.path.join(execution_path, "detection_model-ex-33--loss-4.97.h5"))
detector.setJsonPath(configuration_json=os.path.join(execution_path, "detection_config.json"))
detector.loadModel()
print("Pre-loading Complete\n")

# start monitoring
print("Monitoring room...")
cam_1 = cv2.VideoCapture(1)
cam_2 = cv2.VideoCapture(0)

time_elapsed = 0
prev = time.time()
img_counter = 0
print_waiting_intro = False
fire_pixels_1 = []
fire_pixels_2 = []
minimum_percentage_probability = 20
extinguishing_state = False
print_extinguishing_intro = False
wait_time = 5
while True:
    time_elapsed = time.time() - prev

    ret_1, frame_1 = cam_1.read()
    frame_1 = cv2.flip(frame_1, -1)

    ret_2, frame_2 = cam_2.read()

    if not ret_1:
        print("failed to grab frame")
        break
    cv2.imshow("cam_1", frame_1)

    if not ret_2:
        print("failed to grab frame")
        break
    cv2.imshow("cam_2", frame_2)
    cv2.waitKey(1)

    if time_elapsed > wait_time:  # for every 5 seconds, get a frame from the cam_1
        print("\nProcessing Images...")
        print_waiting_intro = False
        prev = time.time()

        cv2.imwrite(execution_path + r"\monitoring\cam_1.{}.jpg".format(img_counter), frame_1)
        cv2.imwrite(execution_path + r"\monitoring\cam_2.{}.jpg".format(img_counter), frame_2)

        img_path = os.getcwd() + r'\monitoring'
        eng.undistortImgs(img_path, "cam_1.{}.jpg".format(img_counter), "cam_2.{}.jpg".format(img_counter))

        drawn_image_1, output_objects_array_1 = detector.detectObjectsFromImage(
            input_image=img_path + r"\undistorted_cam_1.{}.jpg".format(img_counter),
            input_type="file",
            output_type="array",
            minimum_percentage_probability=minimum_percentage_probability)
        drawn_image_2, output_objects_array_2 = detector.detectObjectsFromImage(
            input_image=img_path + r"\undistorted_cam_2.{}.jpg".format(img_counter),
            input_type="file",
            output_type="array",
            minimum_percentage_probability=minimum_percentage_probability)
        cv2.imwrite(execution_path + r"\monitoring\drawn_image_1.{}.jpg".format(img_counter), drawn_image_1)
        cv2.imwrite(execution_path + r"\monitoring\drawn_image_2.{}.jpg".format(img_counter), drawn_image_2)

        print("\n---------------------")
        print("Result: ", end='')
        if len(output_objects_array_1) == 0 or len(output_objects_array_2) == 0:
            print(colored('Negative', 'green'))
            extinguishing_state = False
            wait_time = 5
            print("---------------------\n")
        elif output_objects_array_2[0] and output_objects_array_1[0]:
            percentage = str(int(output_objects_array_1[0]["percentage_probability"]))
            print(colored(percentage + "% Positive", 'red'))
            print("---------------------\n")


            fire_box_points_1 = output_objects_array_1[0]["box_points"]
            fire_box_points_2 = output_objects_array_2[0]["box_points"]
            fire_pixels_1 = [(fire_box_points_1[0] + fire_box_points_1[2])/2, fire_box_points_1[3]]
            fire_pixels_2 = [(fire_box_points_2[0] + fire_box_points_2[2])/2, fire_box_points_2[3]]
            fire_pixels_1_x = float(fire_pixels_1[0])
            fire_pixels_1_y = float(fire_pixels_1[1])
            fire_pixels_2_x = float(fire_pixels_2[0])
            fire_pixels_2_y = float(fire_pixels_2[1])
            # get world coordinate of cam1 from Matlab script
            cam_world_coordinates = eng.myTriangulate(fire_pixels_1_x, fire_pixels_1_y, fire_pixels_2_x, fire_pixels_2_y)

            my_world_coordinates = np.matmul(R, cam_world_coordinates[0]) + d
            round_my_world_coor = [int(round(my_world_coordinates[0])), int(round(my_world_coordinates[1])), int(round(my_world_coordinates[2]))]
            print("Fire Location: ", colored(round_my_world_coor, 'red'), "\n")

            # decoding coordinates to send to Arduino
            command = ""
            for i in round_my_world_coor:
                if i < 0:
                    i = 0
                if i / 10 < 1:
                    command = command + "00" + str(i)
                elif i / 10 < 10:
                    command = command + "0" + str(i)
                else:
                    command = command + str(i)

            arduinoData.write(command.encode())
            extinguishing_state = True
            wait_time = 20


            img_counter = img_counter + 1

    elif extinguishing_state == True and print_extinguishing_intro == False:
        print("Extinguishing...\n")
        print_extinguishing_intro = True
    elif extinguishing_state == False and print_waiting_intro == False:
        print("Waiting for 5 seconds\n", end='', flush=True)
        print_waiting_intro = True
    elif extinguishing_state == False and print_waiting_intro == True:
        print("#", end='', flush=True)


cam_1.release()
cam_2.release()
cv2.destroyAllWindows()