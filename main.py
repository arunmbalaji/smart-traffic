# sample main.py for testing Microphyton for ESP32 for Sparkfun TB6612FNG Motor Drive for two motors
from machine import Pin, PWM
from time import sleep
from TB6612FNG import Motor
# from worker import task, MT
# import time
import ujson
from umqtt.simple import MQTTClient
import config
# import random
# import sys
import os
frequency = 50

PWMA = 15
AIN2 = 2
AIN1 = 0
STBY = 4
BIN1 = 16
BIN2 = 17
PWMB = 5

ofsetA = 1
ofsetB = 1


motor = Motor(BIN2, BIN1, STBY, AIN1, AIN2, PWMA, PWMB, ofsetA, ofsetB)
zone1_red = Pin(config.ZONE1_RED_PIN, mode=Pin.OUT, pull=None)
zone2_red = Pin(config.ZONE2_RED_PIN, mode=Pin.OUT, pull=None)
zone3_red = Pin(config.ZONE3_RED_PIN, mode=Pin.OUT, pull=None)
zone4_red = Pin(config.ZONE4_RED_PIN, mode=Pin.OUT, pull=None)
zone1_green = Pin(config.ZONE1_GREEN_PIN, mode=Pin.OUT, pull=None)
zone2_green = Pin(config.ZONE2_GREEN_PIN, mode=Pin.OUT, pull=None)
zone3_green = Pin(config.ZONE3_GREEN_PIN, mode=Pin.OUT, pull=None)
zone4_green = Pin(config.ZONE4_GREEN_PIN, mode=Pin.OUT, pull=None)

info = os.uname()
with open("" + config.THING_PRIVATE_KEY, 'r') as f:
    key = f.read()
with open("" + config.THING_CLIENT_CERT, 'r') as f:
    cert = f.read()
client_id = config.THING_ID
topic_sub = f"botid/{config.BOT_ID}"
aws_endpoint = config.MQTT_HOST
ssl_params = {"key":key, "cert":cert, "server_side":False}

def mqtt_connect(client=client_id, endpoint=aws_endpoint, sslp=ssl_params):
    print("CONNECTING TO MQTT BROKER...")
    mqtt = MQTTClient(
        client_id=client,
        server=endpoint,
        port=8883,
        keepalive=4000,
        ssl=True,
        ssl_params=sslp)
    try:
        mqtt.connect()
        print("MQTT BROKER CONNECTION SUCCESSFUL: ", endpoint)
    except Exception as e:
        print("MQTT CONNECTION FAILED: {}".format(e))
        machine.reset()
    return mqtt

# def mqtt_publish(client, topic=topic_pub, message='{"message": "esp32"}'):
#     client.publish(topic, message)
#     # pub_led.value(1)
#     time.sleep(.1)
#     # pub_led.value(0)
#     print("PUBLISHING MESSAGE: {} TO TOPIC: {}".format(message, topic))

def reset_all_lights():
    zone1_red.value(0)
    zone2_red.value(0)
    zone3_red.value(0)
    zone4_red.value(0)
    zone1_green.value(0)
    zone2_green.value(0)
    zone3_green.value(0)
    zone4_green.value(0)

def mqtt_subscribe(topic, message):
    print (message)
    jsonmsg = ujson.loads(message)
    print (jsonmsg)
    cmd = jsonmsg['command']
    if jsonmsg['angle'] is None:
        angle = 0
    else:
        angle = jsonmsg['angle']
    print(cmd)
    if cmd == "FWD":
        print("moving forward")
        motor.forward_with_angle(config.BOT_SPEED, angle)
    elif cmd == "BWD":
        print("moving backward")
        motor.backward(config.BOT_SPEED)
    elif cmd == "RGT":
        print("moving right")
        motor.right(config.BOT_SPEED)
    elif cmd == "LFT":
        print("moving left")
        motor.left(config.BOT_SPEED)
    elif cmd == "STP":
        print("stop motor")
        motor.stop()
    elif cmd == "LIGHTS":
        print("controlling lights")
        if jsonmsg['payload'] is not None:
            if jsonmsg['payload']['ZONE1_RED'] is not None:
                zone1_red.value(jsonmsg['payload']['ZONE1_RED'])
            if jsonmsg['payload']['ZONE2_RED'] is not None:
                zone2_red.value(jsonmsg['payload']['ZONE2_RED'])
            if jsonmsg['payload']['ZONE3_RED'] is not None:
                zone3_red.value(jsonmsg['payload']['ZONE3_RED'])
            if jsonmsg['payload']['ZONE4_RED'] is not None:
                zone4_red.value(jsonmsg['payload']['ZONE4_RED'])
            if jsonmsg['payload']['ZONE1_GREEN'] is not None:
                zone1_green.value(jsonmsg['payload']['ZONE1_GREEN'])
            if jsonmsg['payload']['ZONE2_GREEN'] is not None:
                zone2_green.value(jsonmsg['payload']['ZONE2_GREEN'])
            if jsonmsg['payload']['ZONE3_GREEN'] is not None:
                zone3_green.value(jsonmsg['payload']['ZONE3_GREEN'])
            if jsonmsg['payload']['ZONE4_GREEN'] is not None:
                zone4_green.value(jsonmsg['payload']['ZONE4_GREEN'])
    else:
        print ('no existing command received...')
    print("RECEIVING MESSAGE: {} FROM TOPIC: {}".format(message, topic))

reset_all_lights()
mqtt = mqtt_connect()
mqtt.set_callback(mqtt_subscribe)
mqtt.subscribe(topic_sub)
print('init motor -> move fwd for 1 sec and move back for 1 sec')
motor.forward(500)
sleep(1)
motor.backward(500)
sleep(1)
motor.standby()
motor.run()
while True:
    try:
        mqtt.check_msg()
    except OSError as e:
        print("RECONNECT TO MQTT BROKER")
        mqtt = mqtt_connect()
        mqtt.set_callback(mqtt_subscribe)
        mqtt.subscribe(topic_sub)
    except Exception as e:
        print("A GENERAL ERROR HAS OCCURRED: {}".format(e))