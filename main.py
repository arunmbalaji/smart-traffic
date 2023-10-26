# sample main.py for testing Microphyton for ESP32 for Sparkfun TB6612FNG Motor Drive for two motors
from machine import Pin, PWM
from time import sleep
from TB6612FNG import Motor
from worker import task, MT
import time
import ujson
from umqtt.simple import MQTTClient
import config
import random
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

print("this is bot id 21")
info = os.uname()
with open("" + config.THING_PRIVATE_KEY, 'r') as f:
    key = f.read()
with open("" + config.THING_CLIENT_CERT, 'r') as f:
    cert = f.read()
client_id = config.THING_ID
# topic_pub = "clients/" + client_id + "/sensor01"
topic_sub = f"botid/{config.BOT_ID}"
# cmd = ""
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
# @task
def mqtt_subscribe(topic, message):
    print (message)
    jsonmsg = ujson.loads(message)
    print (jsonmsg)
    # c = yield
    # v = c.v
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
    else:
        print ('no existing command received...')
        # yield
    # sub_led.value(1)
    # time.sleep(.1)
    # sub_led.value(0)
    print("RECEIVING MESSAGE: {} FROM TOPIC: {}".format(message, topic))

@task
def motor_worker(pw):
#   print("Second commit - not moving at all")
  c = yield
  while True:
    # print (f"Checking Command...{cmd}")
    # yield
    if cmd == "forward":
        print("only only only moving forward")
        motor.forward(500)
        yield
    elif cmd == "backward":
        print("moving backward")
        motor.backward(500)
        yield
    elif cmd == "right":
        print("moving right")
        motor.right(500)
        yield
    elif cmd == "left":
        print("moving left")
        motor.left(500)
        yield
    else:
        # print ('no existing command received...')
        yield
  # motor.right(800)
  # sleep(60)
  # c = yield
  # v = c.v
  # while True:
  #   print (f"Checking Command...{c.cmd}")
  #   yield
  #   if cmd == "forward":
  #       print("only only only moving forward")
  #       motor.forward(500)
  #       yield
  #   elif cmd == "backward":
  #       print("moving backward")
  #       motor.backward(500)
  #       yield
  #   elif cmd == "right":
  #       print("moving right")
  #       motor.right(500)
  #       yield
  #   elif cmd == "left":
  #       print("moving left")
  #       motor.left(500)
  #       yield
  #   else:
  #       print ('no existing command received...')
  #       yield
      # motor.standby()
      # sleep(5)

  # print("Finished the execution. Coming out of the loop. Restart to start the loop again.")
  # yield

@task
def mqtt_worker(pw):
  mqtt = mqtt_connect()
  mqtt.set_callback(mqtt_subscribe)
  mqtt.subscribe(topic_sub)
  c=yield
#   v = c.d
#   v.cmd = ""
  while True:
    try:
        mqtt.check_msg()
        yield
    except OSError as e:
        print("RECONNECT TO MQTT BROKER")
        mqtt = mqtt_connect()
        mqtt.set_callback(mqtt_subscribe)
        mqtt.subscribe(topic_sub)
    except Exception as e:
        print("A GENERAL ERROR HAS OCCURRED: {}".format(e))
        # machine.reset()
    # print('out of mqtt worker')
    yield

# mt=MT(3)                # we need only 2 workers
# mt.worker(motor_worker, ())       # worker for keyboard (in)
# mt.worker(mqtt_worker, ()) # worker for LED (out)
# # mt.worker(mqtt_subscribe, ()) # worker for LED (out)
# mt.start()
print(config.BOT_SPEED)
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
        # yield
    except OSError as e:
        print("RECONNECT TO MQTT BROKER")
        mqtt = mqtt_connect()
        mqtt.set_callback(mqtt_subscribe)
        mqtt.subscribe(topic_sub)
    except Exception as e:
        print("A GENERAL ERROR HAS OCCURRED: {}".format(e))
        # machine.reset()
    # print('out of mqtt worker')
    # yield