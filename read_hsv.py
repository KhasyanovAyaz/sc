import cv2
import numpy
import math
from paho.mqtt.client import Client
from time import sleep

message1 = ''
hypotenuse_9 = 0
hypotenuse_7 = 0
angle_degrees = 0
cathet = 0
x1_9 = 0
x4_9 = 0
y1_9 = 0
y4_9 = 0
x1_7 = 0
x4_7 = 0
y1_7 = 0
y4_7 = 0
cosinus_9 = 0
cosinus_7 = 0
angle_9 = 0
angle_7 = 0

def conect_status(device, userdata, flags, result):
    if result == 0:
        print("Устройство подключенно")
    else:
        print("Устройство не подключенно")

def subscribe_status(device, userdata, mid, qos):
    print('Устройство подписано на ', mid, "топик")


def recive_message(device, userdata, message):
    global message1
    message1 = message.payload.decode()
    message2 = message.payload.decode()
    print(message1)
    anglerun_1 = int(angle_degrees_7) - int(message1)
    if anglerun_1 > 180:
        anglerun_2 = 360 - anglerun_1
        if anglerun_1 > 0:
            anglerun_2 = -anglerun_2
        anglerun_1 = anglerun_2
    device.publish("ayazkhasyanov/align_camera", anglerun_1)

    if message2 == "get":
        device.publish('ayazkhasyanov/align_camera', angle_degrees_7)


def read_values_from_file(filename):
    file = open(filename, 'r')
    values = file.read()
    print(values)
    values_split = values.split(', ')
    print(values_split)
    for number in range(6):
        values_split[number] = int(values_split[number])
    print(values_split)
    file.close()
    return values_split


def find_center(x, y, width, height, image):
    x_center = x + width // 2
    y_center = y + height // 2
    cv2.circle(image, (x_center, y_center), 5, (0, 0, 255), -1)
    return x_center, y_center


H_up, H_down, S_up, S_down, V_up, V_down = read_values_from_file('HSV.txt')
HSV_up = [H_up, S_up, V_up]
HSV_down = [H_down, S_down, V_down]
np_HSV_up = numpy.array(HSV_up)
np_HSV_down = numpy.array(HSV_down)
cap = cv2.VideoCapture(0)

key = -1
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
x_center, xc = 0, 0
y_center, yc = 0, 0

device = Client('ayazkhasyanov')
device.username_pw_set('ayazkhasyanov', 'Khasyanov1')
device.connect('mqtt.pi40.ru', 1883)
device.subscribe('ayazkhasyanov/get_angle')
device.subscribe('ayazkhasyanov/robot')
device.on_connect = conect_status
device.on_subscribe = subscribe_status
device.on_message = recive_message
device.loop_start()

while key == -1:
    isRead, image = cap.read()
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners, ids, service = cv2.aruco.detectMarkers(image_gray, dictionary)
    cv2.aruco.drawDetectedMarkers(image, corners)
    for i in range(len(corners)):
        marker_conters = corners[i]
        ids = ids[[0]]
        cv2.putText(image, str(ids), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 3)
        print(ids)
        if ids == 9:
            x1_9, y1_9 = marker_conters[0][0]
            cv2.circle(image, (int(x1_9), int(y1_9)), 15, (0, 0, 0), -1)
            x2_9, y2_9 = marker_conters[0][1]
            cv2.circle(image, (int(x2_9), int(y2_9)), 15, (0, 255, 0), -1)
            x3_9, y3_9 = marker_conters[0][2]
            cv2.circle(image, (int(x3_9), int(y3_9)), 15, (255, 0, 0), -1)
            x4_9, y4_9 = marker_conters[0][3]
            cv2.circle(image, (int(x4_9), int(y4_9)), 15, (255, 255, 255), -1)
            xc_9 = (x1_9 + x3_9) / 2
            yc_9 = (y1_9 + y3_9) / 2
            xc_9 = int(xc_9)
            yc_9 = int(yc_9)
            cv2.circle(image, (xc_9, yc_9), 15, (255, 0, 0), -1)
            cv2.line(image, (int(x1_9), int(y1_9)), (int(x4_9), int(y4_9)), (0, 0, 255), 5)
            hypotenuse_9 = math.sqrt((x4_9 - x1_9) ** 2 + (y4_9 - y1_9) ** 2)
            cv2.line(image, (int(x4_9), int(y1_9)), (int(x4_9), int(y4_9)), (0, 255, 0), 5)
            cathet_9 = math.sqrt((y1_9 - y4_9) ** 2)
            cv2.putText(image, str(xc_9) + ',' + str(yc_9), (int(xc_9), int(yc_9)), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 3)
            cosinus_9 = cathet_9 / hypotenuse_9
            angle_9 = math.acos(cosinus_9)
            angle_degrees_9 = math.degrees(angle_9)
            angle_degrees_9 = int(angle_degrees_9)
            if int(x1_9) > int(x4_9) and int(y1_9) > int(y4_9):
                angle_degrees_9 = 180 - angle_degrees_9
            elif int(x1_9) < int(x4_9) and int(y1_9) > int(y4_9):
                angle_degrees_9 = 180 + angle_degrees_9
            elif int(x1_9) < int(x4_9) and int(y1_9) < int(y4_9):
                angle_degrees_9 = 360 - angle_degrees_9
            cv2.putText(image, str(angle_degrees_9), (int(x4_9), int(y4_9)), cv2.FONT_HERSHEY_COMPLEX, 1,
                        (255, 255, 0), 5)
        if ids == 7:
            x1_7, y1_7 = marker_conters[0][0]
            cv2.circle(image, (int(x1_7), int(y1_7)), 15, (0, 0, 0), -1)
            x2_7, y2_7 = marker_conters[0][1]
            cv2.circle(image, (int(x2_7), int(y2_7)), 15, (0, 255, 0), -1)
            x3_7, y3_7 = marker_conters[0][2]
            cv2.circle(image, (int(x3_7), int(y3_7)), 15, (255, 0, 0), -1)
            x4_7, y4_7 = marker_conters[0][3]
            cv2.circle(image, (int(x4_7), int(y4_7)), 15, (255, 255, 255), -1)
            xc_7 = (x1_7 + x3_7) / 2
            yc_7 = (y1_7 + y3_7) / 2
            xc_7 = int(xc_7)
            yc_7 = int(yc_7)
            cv2.circle(image, (xc_7, yc_7), 15, (255, 0, 0), -1)
            cv2.line(image, (int(x1_7), int(y1_7)), (int(x4_7), int(y4_7)), (0, 0, 255), 5)
            hypotenuse_7 = math.sqrt((x4_7 - x1_7) ** 2 + (y4_7 - y1_7) ** 2)
            cv2.line(image, (int(x4_7), int(y1_7)), (int(x4_7), int(y4_7)), (0, 255, 0), 5)
            cathet_7 = math.sqrt((y1_7 - y4_7) ** 2)
            cv2.putText(image, str(xc_7) + ',' + str(yc_7), (int(xc_7), int(yc_7)), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 3)

            print(cathet_7, hypotenuse_7)
            cosinus_7 = cathet_7 / hypotenuse_7
            angle_7 = math.acos(cosinus_7)
            angle_degrees_7 = math.degrees(angle_7)
            angle_degrees_7 = int(angle_degrees_7)
            if int(x1_7) > int(x4_7) and int(y1_7) > int(y4_7):
                angle_degrees_7 = 180 - angle_degrees_7
            elif int(x1_7) < int(x4_7) and int(y1_7) > int(y4_7):
                angle_degrees_7 = 180 + angle_degrees_7
            elif int(x1_7) < int(x4_7) and int(y1_7) < int(y4_7):
                angle_degrees_7 = 360 - angle_degrees_7
            cv2.putText(image, str(angle_degrees_7), (int(x4_7), int(y4_7)), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0),
                        5)
            print('test:',message1)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    mask = cv2.inRange(image_hsv, np_HSV_down, np_HSV_up)
    conturs, service = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image, conturs, -1, (255, 0, 0), 3)
    for c in conturs:
        x, y, width, height = cv2.boundingRect(c)
        if width * height > 1000:
            cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)
            x_center, y_center = find_center(x, y, width, height, image)
            cv2.putText(image, 'Центора первого арукомаркера:' + str(x_center) + ',' + str(y_center), (0, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
    key = cv2.waitKey(30)
    cv2.imshow('window', image)


cap.release()
