# sample main.py for testing Microphyton for ESP32 for Sparkfun TB6612FNG Motor Drive for two motors
from machine import Pin, PWM
from time import sleep
from TB6612FNG import Motor
from worker_lite import task, MT
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
topic_pub = "clients/" + client_id + "/sensor01"
topic_sub = "clients/general"
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

def mqtt_publish(client, topic=topic_pub, message='{"message": "esp32"}'):
    client.publish(topic, message)
    # pub_led.value(1)
    time.sleep(.1)
    # pub_led.value(0)
    print("PUBLISHING MESSAGE: {} TO TOPIC: {}".format(message, topic))

def mqtt_subscribe(topic, message):
    message = ujson.loads(message)
    # sub_led.value(1)
    time.sleep(.1)
    # sub_led.value(0)
    print("RECEIVING MESSAGE: {} FROM TOPIC: {}".format(message, topic))

@task
def motor_worker(pw):
  # print("Second commit - not moving at all")
  # motor.right(800)
  # sleep(60)

  print("only only only moving forward")
  motor.forward(500)
  sleep(10)

  print("moving backward")
  motor.backward(500)
  sleep(5)


  print("moving right")
  motor.right(500)
  sleep(20)


  print("moving left")
  motor.left(500)
  sleep(20)

  motor.standby()
  sleep(5)

  print("Finished the execution. Coming out of the loop. Restart to start the loop again.")

@task
def mqtt_worker(pw):
  mqtt = mqtt_connect()
  mqtt.set_callback(mqtt_subscribe)
  mqtt.subscribe(topic_sub)
  try:
      mqtt.check_msg()
      # sensor.measure()
      temp = random.random()
      hum = random.random()
      msg = ujson.dumps({
          "client": client_id,
          "device": {
              "uptime": time.ticks_ms(),
              "hardware": info[0],
              "firmware": info[2]
          },
          "sensors": {
              "temperature": temp,
              "humidity": hum,
          },
          "status": "online",
      })
      mqtt_publish(client=mqtt, message=msg)
      time.sleep(2)
  except OSError as e:
      print("RECONNECT TO MQTT BROKER")
      mqtt = mqtt_connect()
      mqtt.set_callback(mqtt_subscribe)
      mqtt.subscribe(topic_sub)
  except Exception as e:
      print("A GENERAL ERROR HAS OCCURRED: {}".format(e))
      # machine.reset()

mt=MT(2)                # we need only 2 workers
mt.worker(motor_worker, ())       # worker for keyboard (in)
mt.worker(mqtt_worker, ()) # worker for LED (out)
mt.start()