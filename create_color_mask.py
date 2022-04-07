import cv2
import numpy

cap=cv2.VideoCapture("blue_car.mp4")

H_up,S_up,V_up=140,255,255
H_down,S_down,V_down=120,70,70
HSV_up=[H_up, S_up, V_up]
HSV_down=[H_down, S_down, V_down]
np_HSV_up=numpy.array(HSV_up)
np_HSV_down=numpy.array(HSV_down)

for number in range(330):
    isRead,image=cap.read()
    image_hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV_FULL)
    mask=cv2.inRange(image_hsv, np_HSV_down, np_HSV_up)
    cv2.imshow('window_mask', mask)
    cv2.imshow('window',image)
    cv2.waitKey(20)
cap.release()
