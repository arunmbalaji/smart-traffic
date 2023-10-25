# sample main.py for testing Microphyton for ESP32 for Sparkfun TB6612FNG Motor Drive for two motors
from machine import Pin, PWM
from time import sleep
from TB6612FNG import Motor


def test_motors():
    print("starting the testing")
    sleep(5)

    print("moving forward")
    motor.forward(500)
    sleep(5)

    print("moving backward")
    motor.backward(500)
    sleep(5)

    print("moving right")
    motor.right(500)
    sleep(5)

    print("moving left")
    motor.left(500)
    sleep(5)

    motor.brake()
    sleep(5)

    motor.stop()
    sleep(2)

    motor.standby()
    sleep(2)

    motor.run()
    sleep(2)


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

print("this is bot id 22")

test_motors()

print("Finished the execution. Coming out of the loop. Restart to start the loop again.")
