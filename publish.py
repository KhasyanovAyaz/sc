from paho.mqtt.client import Client
import random

def recive_message(device, userdata, message):
    t_h= "27, 35%"
    t1_h1 = "25, 37%"
    print(message.payload.decode())
    device.publish("ayazkhasyanov/2",t_h)
    device.publish("ayazkhasyanov/2", t1_h1)

#def conect_status(device, userdata, flags, result):
    #if result == 0:
        #print("Устройство подключенно")
    #else:
        #print("Устройство не подключенно")

def subscribe_status(device, userdata, mid, qos):
    print('Устройство подписано на ', mid, "топик")


device = Client('ayazkhasyanov1')
device.username_pw_set('ayazkhasyanov', 'Khasyanov1')
device.connect('mqtt.pi40.ru', 1883)
device.subscribe('ayazkhasyanov/1')
#device.on_connect = conect_status
device.on_subscribe = subscribe_status
device.on_message = recive_message
device.loop_forever()