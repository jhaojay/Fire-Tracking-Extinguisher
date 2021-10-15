import cv2


def getTopPixel(image_1, image_2):
    # get top pixels from a pair of images by clicking on it. Return 2 arrays of arrays

    top_pixels_1 = []
    top_pixels_2 = []

    clone_1 = image_1.copy()
    clone_2 = image_2.copy()

    def click_and_crop_1(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("image 1: ", x, y)
            top_pixels_1.append([x,y])
            cv2.circle(image_1, (x, y), radius=4, color=(0, 255, 0), thickness=-1)

    def click_and_crop_2(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("image 2: ", x, y)
            top_pixels_2.append([x, y])
            cv2.circle(image_2, (x, y), radius=4, color=(0, 255, 0), thickness=-1)

    while True:
        cv2.setMouseCallback("image_1", click_and_crop_1)
        cv2.imshow("image_1", image_1)

        cv2.setMouseCallback("image_2", click_and_crop_2)
        cv2.imshow("image_2", image_2)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("r"):
            print("Reset image 1")
            image_1 = clone_1.copy()
            top_pixels_1.clear()
        elif key == ord("f"):
            print("Reset image 2")
            image_2 = clone_2.copy()
            top_pixels_2.clear()
        elif key%256 == 32:  # Space bar
            break

    cv2.destroyAllWindows()
    return top_pixels_1, top_pixels_2


# image_1 = cv2.imread("opencv_frame_0.png")
# image_2 = cv2.imread("2.png")
# print(getTopPixel(image_1, image_2))
