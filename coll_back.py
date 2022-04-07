from paho.mqtt.client import Client
import time

def recive_message(device, userdata, message):
    print(message.payload.decode())
    time.sleep(1)
    device.publish("ayazkhasyanov/1","go")

#def conect_status(device, userdata, flags, result):
    #if result == 0:
        #print("Устройство подключенно")
    #else:
        #print("Устройство не подключенно")

def subscribe_status(device, userdata, mid, qos):
    print('Устройство подписано на ', mid, "топик")


device = Client('ayazkhasyanov')
device.username_pw_set('ayazkhasyanov', 'Khasyanov1')
device.connect('mqtt.pi40.ru', 1883)
device.subscribe('ayazkhasyanov/2')
#device.on_connect = conect_status
device.on_subscribe = subscribe_status
device.publish("ayazkhasyanov/1", "go")
device.on_message = recive_message
device.loop_forever()
