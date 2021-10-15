import cv2
import matlab.engine
import os
import shutil
import sys


def takeSteroPic(times, path):

    cam_1 = cv2.VideoCapture(1)
    cam_2 = cv2.VideoCapture(0)

    img_counter = 0

    while img_counter < times:
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
            break
        elif k % 256 == 32:
            # SPACE pressed
            img_name_1 = path + r"\cam_1.{}.png".format(img_counter)
            cv2.imwrite(img_name_1, cv2.flip(frame_1, -1))
            print("{} written!".format(img_name_1))

            img_name_2 = path + r"\cam_2.{}.png".format(img_counter)
            cv2.imwrite(img_name_2, frame_2)
            print("{} written!".format(img_name_2))
            img_counter += 1

    cam_1.release()
    cam_2.release()

    cv2.destroyAllWindows()


def emptyFolder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


img_folder = os.getcwd() + r"\CoordinateCalibrationImages"
print("Chess pieces are about to be taken, are you sure you want to empty the CoordinateCalibrationImages folder first?")
val = input("Enter your value: y means Yes.")
if val == 'y':
    emptyFolder(img_folder)
else:
    print("Program terminated.")
    sys.exit()



takeSteroPic(4, img_folder)

#================ generate undistorted images using MatLab
#
print("\nGenerating undistorted images using MatLab...")
eng = matlab.engine.start_matlab()
matlab_code_path = os.getcwd() + r'\MatlabCode'
eng.cd(matlab_code_path)
img_path = os.getcwd() + r'\CoordinateCalibrationImages'

for i in range(4):
    eng.undistortImgs(img_path, "cam_1.{}.png".format(i), "cam_2.{}.png".format(i))
print("Undistorted images generated.\n")