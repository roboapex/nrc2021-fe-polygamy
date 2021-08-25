#!/usr/bin/env python3

print('import')
import time
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_3, INPUT_4

leftUltra = UltrasonicSensor(INPUT_3)
rightUltra = UltrasonicSensor(INPUT_4)

leftMotor = LargeMotor(OUTPUT_A)
rightMotor = LargeMotor(OUTPUT_D)


speed = 50
integral = 0
last_error = 0
kp = 0.2
ki = 0.0
kd = 0
while True:
    if leftUltra.distance_centimeters > 50:
        leftDist = 50
    else:
        leftDist = leftUltra.distance_centimeters
    if rightUltra.distance_centimeters > 50:
        rightDist = 50
    else:
        rightDist = rightUltra.distance_centimeters
    error = leftDist - rightDist
    integral = error + integral
    derivative = error - last_error
    value = error * kp + integral * ki + derivative * kd
    if speed-value > 90:
        leftSpeed = 90
    elif speed-value < -90:
        leftSpeed = -90
    else:
        leftSpeed = speed-value

    if speed+value > 90:
        rightSpeed = 90
    elif speed+value < -90:
        rightSpeed = -90
    else:
        rightSpeed = speed+value
    leftMotor.on(leftSpeed,brake=True,block=False)
    rightMotor.on(rightSpeed,brake=True,block=False)
    lastError = error



