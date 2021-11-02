#!/usr/bin/env micropython

print('import')
import time
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, OUTPUT_B, MediumMotor
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_1
print('done')

frontUltra = UltrasonicSensor(INPUT_1)
leftUltra = UltrasonicSensor(INPUT_2)
rightUltra = UltrasonicSensor(INPUT_3)

leftMotor = MediumMotor(OUTPUT_B)
rightMotor = MediumMotor(OUTPUT_D)

frontDist = 40
leftDist = 40
rightDist = 40

speed = 40
integral = 0
last_error = 0
kp = 3
ki = 0
kd = 0

while frontDist > 10:
    frontDist = min(int(frontUltra.distance_centimeters),40)
    if frontDist < 10:
        break
    leftDist = min(int(leftUltra.distance_centimeters),40)
    rightDist = min(int(rightUltra.distance_centimeters),40)
    print("{} {} {}".format(leftDist, rightDist, leftDist-rightDist))

    error = leftDist - rightDist
    integral = error + integral
    derivative = error - last_error
    value = error * kp + integral * ki + derivative * kd

    leftSpeed = -speed + value
    if leftSpeed > 90:
        leftSpeed = 90
    elif leftSpeed < -90:
        leftSpeed = -90
    rightSpeed = speed + value
    if rightSpeed > 90:
        rightSpeed = 90
    elif rightSpeed < -90:
        rightSpeed = -90
    print("{} {}".format(leftSpeed,rightSpeed))
    leftMotor.on(leftSpeed,brake=False,block=False)
    rightMotor.on(rightSpeed,brake=False,block=False)
    lastError = error
print('end')
    