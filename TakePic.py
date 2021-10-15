import cv2

cam_1 = cv2.VideoCapture(1)
cam_2 = cv2.VideoCapture(0)

img_counter = 0

while True:
    ret_1, frame_1 = cam_1.read()
    ret_2, frame_2 = cam_2.read()

    if not ret_1:
        print("failed to grab frame")
        break
    cv2.imshow("cam_1",cv2.flip(frame_1, -1))

    if not ret_2:
        print("failed to grab frame")
        break
    cv2.imshow("cam_2", frame_2)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name_1 = "cam1/opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name_1, cv2.flip(frame_1, -1))
        print("{} written!".format(img_name_1))

        img_name_2 = "cam2/opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name_2, frame_2)
        print("{} written!".format(img_name_2))
        img_counter += 1

cam_1.release()
cam_2.release()

cv2.destroyAllWindows()