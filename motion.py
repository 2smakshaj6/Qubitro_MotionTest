import paho.mqtt.publish as publish
from bluepy import btle, thingy52
import paho.mqtt.client as mqtt
import binascii
import json
import time
import os
import argparse
import binascii
import logging
import signal, sys
global args
global thingy
args = None
thingy = None

#Change the below parm as per yours
MAC_ADDRESS = "DE:A5:4A:51:5B:C3"
broker_host = "broker.qubitro.com"
broker_port = 8883
device_id = "93771eb9-62af-428d-9cf2-341a41fa1944"
device_token = "1jEXaqYW5k$$Q3JAwHkSkBTCKuDPzSIRSfQRM8DN"
###############################################################


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Qubitro!")
        client.on_publish = on_publish
    else:
        print("Failed to connect, visit: https://docs.qubitro.com/client-guides/connect-device/mqtt\n return code:", rc)

def on_publish(client, obj, publish):
    print("Published: " + str(payload))

def on_disconnect(client, userdata, rc):
    # E.g. reconnect to the broker
    print("Disconnection returned result:" + str(rc))


class MQTTDelegate(btle.DefaultDelegate):

    def handleNotification(self, hnd, data):

        #Debug print repr(data)
        #for i in range(1):
        hnd == thingy52.e_temperature_handle
        teptep = binascii.b2a_hex(data)
        Temp = self._str_to_int(teptep[:-2]) + int(teptep[-2:], 16) / 100.0
        print('Temperature', Temp, '°C')
        payload ={"Temperature": Temp}

        client.publish(device_id, payload=json.dumps(payload))
       

    def _str_to_int(self, s):
        """ Transform hex str into int. """
        i = int(s, 16)
        if i >= 2**7:
            i -= 2**8
        return i
   


print('Try to connect to ' + MAC_ADDRESS)
#thingy = thingy52.Thingy52(MAC_ADDRESS)
thingy = thingy52.Thingy52("DE:A5:4A:51:5B:C3")
connected = False
client = mqtt.Client(client_id=device_id)
client.tls_set_context(context=None)
client.username_pw_set(username=device_id, password=device_token)
client.connect(broker_host, broker_port, 10)
client.on_connect = on_connect

while not connected:
    thingy.sound.enable()
    thingy.sound.configure(speaker_mode=0x03)
    thingy.sound.play_speaker_sample(1)
    thingy.ui.enable()
    thingy.ui.set_led_mode_breathe(0x01, 50, 500) # color 0x01 = RED, intensity, delay between breathes
   
    thingy.setDelegate(MQTTDelegate())
    thingy.environment.enable()
    thingy.environment.configure(temp_int=1000)
    thingy.environment.set_temperature_notification(True)
    thingy.environment.enable()
    thingy.ui.enable()
    time.sleep(5)
