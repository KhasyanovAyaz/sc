from paho.mqtt.client import Client

def recive_message(device, userdata, message):
    print(message.payload.decode())

device = Client('ayazkhasyanov')
device.username_pw_set('ayazkhasyanov', 'Khasyanov1')
device.connect('mqtt.pi40.ru', 1883)
device.subscribe('ayazkhasyanov/align_camera')
device.on_message = recive_message
device.publish("ayazkhasyanov/align_robot", 45)
device.loop_forever()