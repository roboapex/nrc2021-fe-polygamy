#!/usr/bin/env python3

print('import')
import time
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_3, INPUT_4, INPUT_1

frontUltra = UltrasonicSensor(INPUT_1)
leftUltra = UltrasonicSensor(INPUT_3)
rightUltra = UltrasonicSensor(INPUT_4)

leftMotor = LargeMotor(OUTPUT_A)
rightMotor = LargeMotor(OUTPUT_D)


speed = 50
integral = 0
last_error = 0
kp = 0.5
ki = 0.01
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
    if frontUltra.distance_centimeters > 50:
        frontDist = 50
    else:
        frontDist = frontUltra.distance_centimeters
    if frontDist < 10 :
        if leftDist < rightDist:
            while frontDist < 40:
                leftMotor.on(50,brake=True,block=False)
                rightMotor.on(20,brake=True,block=False)
        elif leftDist > rightDist:
            while frontDist < 40:
                leftMotor.on(20,brake=True,block=False)
                rightMotor.on(50,brake=True,block=False)
        else:
            pass
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



