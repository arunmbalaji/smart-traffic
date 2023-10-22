# sample main.py for testing Microphyton for ESP32 for Sparkfun TB6612FNG Motor Drive for two motors
from machine import Pin, PWM
from time import sleep
from TB6612FNG import Motor

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


print("not moving at all")
print("just adding one more statement")
# motor.right(800)
# sleep(60)

# print("only only only moving forward")
# motor.forward(500)
# sleep(10)

# print("moving backward")
# motor.backward(500)
# sleep(5)


# print("moving right")
# motor.right(500)
# sleep(20)


# print("moving left")
# motor.left(500)
# sleep(20)


# print("moving forward")
# motor.forward(500)
# sleep(10)

# print("moving right")
# motor.right(500)
# sleep(4)

# print("moving forward")
# motor.forward(500)
# sleep(10)

# print("moving right")
# motor.right(500)
# sleep(4)

# print("moving forward")
# motor.forward(500)
# sleep(10)

# motor.backward(600)
# sleep(10)

# print("moving right")
# motor.right(700)
# sleep(10)

# motor.left(800)
# sleep(10)

motor.brake()
sleep(5)

motor.stop()
sleep(5)

motor.standby()
sleep(5)

motor.run()
sleep(5)
