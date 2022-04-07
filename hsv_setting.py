import cv2
import numpy


def create_window():
    cv2.namedWindow("window_hsv")
    cv2.resizeWindow("window_hsv", 700, 400)
    cv2.createTrackbar('H_up', "window_hsv", 255, 255, print)
    cv2.createTrackbar('H_down', "window_hsv", 0, 255, print)
    cv2.createTrackbar('S_up', "window_hsv", 255, 255, print)
    cv2.createTrackbar('S_down', "window_hsv", 0, 255, print)
    cv2.createTrackbar('V_up', "window_hsv", 255, 255, print)
    cv2.createTrackbar('V_down', "window_hsv", 0, 255, print)


def get_slider_position():
    H_up = cv2.getTrackbarPos('H_up', "window_hsv")
    H_down = cv2.getTrackbarPos('H_down', "window_hsv")
    S_up = cv2.getTrackbarPos('S_up', "window_hsv")
    S_down = cv2.getTrackbarPos('S_down', "window_hsv")
    V_up = cv2.getTrackbarPos('V_up', "window_hsv")
    V_down = cv2.getTrackbarPos('V_down', "window_hsv")
    return H_up, H_down, S_up, S_down, V_up, V_down


def write_hsv_values(filename):
    file = open(filename, 'w')
    file.write(str(H_up))
    file.write(', ')
    file.write(str(H_down))
    file.write(', ')
    file.write(str(S_up))
    file.write(', ')
    file.write(str(S_down))
    file.write(', ')
    file.write(str(V_up))
    file.write(', ')
    file.write(str(V_down))


cap = cv2.VideoCapture(0)

key = -1

create_window()

while key == -1:
    isRead, image = cap.read()
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    H_up, H_down, S_up, S_down, V_up, V_down = get_slider_position()
    # print(H_up)
    HSV_up = [H_up, S_up, V_up]
    HSV_down = [H_down, S_down, V_down]
    np_HSV_up = numpy.array(HSV_up)
    np_HSV_down = numpy.array(HSV_down)
    mask = cv2.inRange(image_hsv, np_HSV_down, np_HSV_up)
    cv2.imshow('window_mask', mask)
    cv2.imshow('window', image)
    key = cv2.waitKey(20)
cap.release()

write_hsv_values('HSV.txt')
