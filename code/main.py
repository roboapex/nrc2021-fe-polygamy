#!/usr/bin/env python3
import time
import asyncio

from ev3dev2.display import Display
from ev3dev2.motor import MediumMotor, OUTPUT_B, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.port import LegoPort
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4, UltrasonicSensor

from camera import colour

frontUltra = UltrasonicSensor(INPUT_1)
leftUltra = UltrasonicSensor(INPUT_2)
rightUltra = UltrasonicSensor(INPUT_3)

leftMotor = MediumMotor(OUTPUT_B)
rightMotor = MediumMotor(OUTPUT_D)

sped = 30

green = []
red = []

# Sigmap 1 is trained on red
# Sigmap 2 is trained on green

def forward(speed, distance, brake):
    # Figure out how many rotations is 1m
    # Use ratio to get the correct rot to m
    # Move robot and flow to next step in a smooth way
    rotPm = 3.45
    leftMotor.on_for_rotations(speed, distance * rotPm * -1, brake=brake, block=False)
    rightMotor.on_for_rotations(speed, distance * rotPm  , brake=brake, block=True)

def forwardTill(speed,dist):
    while frontUltra.distance_centimeters > dist:
        leftMotor.on((speed)*-1,brake=True,block=False)
        rightMotor.on((speed),brake=True,block=False)

    leftMotor.stop()
    rightMotor.stop()

def spinTurn(speed,dist):
    ratio = 0.87 / 2
    leftMotor.on_for_rotations(-speed, ratio * dist, brake=True, block=False)
    rightMotor.on_for_rotations(-speed, ratio * dist, brake=True, block=True)

def section():
    colour(1) = green
    colour(2) = red
    if (red != []) and (green == []):
        if red[1] > 157.5:
            spinTurn(sped, 1)
            forwardTill(sped, 5)
            forward(sped, 20, True)
        else:
            spinTurn(sped, 1)
            forwardTill(sped, 15)
            forward(sped, 20, True)
    elif (red == []) and (green != []):
        if green[1] < 157.5:
            spinTurn(-sped, 1)
            forwardTill(sped, 5)
            forward(sped, 20, True)
        else:
            spinTurn(-sped, 1)
            forwardTill(sped, 15)
            forward(sped, 20, True)
    else: #no blocks detected
        forwardTill(sped, 33, True)

loop = asyncio.get_event_loop() #Run ultrasonic check alongside main code

async def ultrasonic():
    speed = -20
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

        if frontDist < 10:
            if leftDist < rightDist:
                while frontDist < 40:
                    leftMotor.on(50, brake=True, block=False)
                    rightMotor.on(20, brake=True, block=False)
            elif leftDist > rightDist:
                while frontDist < 40:
                    leftMotor.on(20, brake=True, block=False)
                    rightMotor.on(50, brake=True, block=False)
            else:
                pass
        error = leftDist - rightDist
        integral = error + integral
        derivative = error - last_error
        value = error * kp + integral * ki + derivative * kd
        if speed - value > 90:
            leftSpeed = 90
        elif speed - value < -90:
            leftSpeed = -90
        else:
            leftSpeed = speed - value

        if speed + value > 90:
            rightSpeed = 90
        elif speed + value < -90:
            rightSpeed = -90
        else:
            rightSpeed = speed + value
        leftMotor.on(leftSpeed, brake=True, block=False)
        rightMotor.on(rightSpeed, brake=True, block=False)

        await asyncio.sleep(1)  # Run every 1 second

loop.create_task(ultrasonic())

for i in range(12):
    forwardTill(sped, 70)
    spinTurn(sped, 1)
    section()
    section()
    section()

loop.run_forever()