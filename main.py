#!/usr/bin/env pybricks-micropython
import time

from pybricks.ev3devices import (ColorSensor, GyroSensor, InfraredSensor,
                                 Motor, TouchSensor, UltrasonicSensor)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import Font, ImageFile, SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait

# Import smbus drivers for i2c camera
from smbus import SMBus

from ev3dev2.port import LegoPort
from ev3dev2.sensor import INPUT_1

# Set LEGO port for Pixy2 on input port 1
in1 = LegoPort(INPUT_1)
in1.mode = 'other-i2c'
# Short wait for the port to get ready
time.sleep(0.5)

 # Settings for I2C (SMBus(3) for INPUT_1)
bus = SMBus(3)
address = 0x54

# Request and read protocal for camera
data = [174, 193, 14, 0]
bus.write_i2c_block_data(address, 0, data)
block = bus.read_i2c_block_data(address, 0, 13)


# Create your objects here.
big_font = Font(size=18, bold=True)
ev3 = EV3Brick()
last_error = 0

# Motors
leftMotor = Motor(Port.C)
rightMotor = Motor(Port.B)
rightMedMotor = Motor(Port.A)
leftMedMotor = Motor(Port.D)

# Sensors
rightSensor = ColorSensor(Port.S1)
middleSensor = ColorSensor(Port.S2)
leftSensor = ColorSensor(Port.S3)
buttonSensor = TouchSensor(Port.S4)

# TODO remove irman things
ev3.speaker.set_volume(20, which='Beep')
ev3.speaker.set_volume(100, which='PCM')
ev3.speaker.set_speech_options(language='en', voice='m2', speed=180, pitch=50)
'''
ev3.speaker.play_notes(['D#4/4', 'F4/4', 'G4/4', 'G#4/8', 'A#4/4', 'R/16',
                        'G#4/4', 'D#4/8', 'C#4/8', 'D#4/8', 'C#4/4', 'R/8',
                        'G4/4', 'D#4/8', 'C#4/8', 'D#4/8', 'C#4/4', 'R/8',
                        'B4/4', 'B4/8', 'B4/8', 'G#4/8', 'B4/8', 'C#5/8', 'B4/8', 'D#5/2', 'R/32',
                        'D#4/8', 'D#4/8', 'C#5/4', 'R/32',
                        'D#4/8', 'D#4/8', 'C#5/4', 'R/32',
                        'D#4/4', 'Db4/4', 'D#4/4', 'Db4/4', 'D#4/4', 'Db4/4', 'D#4/4', 'Db4/4',
                        'B4/8', 'Bb4/8', 'B4/8', 'Bb4/8', 'G#4/8', 'G#4/4', 'Gb4/8', 'G#4/4', 'R/4',
                        'G#4/4', 'Gb4/8', 'G#4/4', 'R/4',
                        'G#4/4', 'Gb4/8', 'G#4/4', 'R/4', ], tempo=120)
'''
# Functions


def MoveToAngle(leftAngle, rightAngle, leftSpeed, rightSpeed):
    leftMotor.reset_angle(0)
    rightMotor.reset_angle(0)
    leftMotor.run(leftSpeed)
    rightMotor.run(rightSpeed)
    while (abs(leftMotor.angle()) < abs(leftAngle)) or (abs(rightMotor.angle()) < abs(rightAngle)):
        if abs(rightMotor.angle()) >= abs(rightAngle):
            rightMotor.hold()
        if abs(leftMotor.angle()) >= abs(leftAngle):
            leftMotor.hold()
    leftMotor.hold()
    rightMotor.hold()


def MoveStalled(leftDC, rightDC):
    leftMotor.dc(leftDC)
    rightMotor.dc(rightDC)

    while True:
        if leftMotor.control.stalled():
            leftMotor.stop()
            rightMotor.stop()
            break
        if rightMotor.control.stalled():
            leftMotor.stop()
            rightMotor.stop()
            break


def SinglePTrack(sensorPort, threshold, kp, speed):
    if sensorPort == 3:
        ref = leftSensor.reflection()
        leftMotor.run(speed + ((ref - threshold) * kp))
        rightMotor.run(speed - ((ref - threshold) * kp))
    elif sensorPort == 2:
        ref = middleSensor.reflection()
        leftMotor.run(speed + ((ref - threshold) * kp))
        rightMotor.run(speed - ((ref - threshold) * kp))
    else:
        ref = rightSensor.reflection()
        leftMotor.run(speed + ((ref - threshold) * kp))
        rightMotor.run(speed - ((ref - threshold) * kp))


def SinglePTrackTillJunction(junctionPort, junctionThreshold, trackingPort, trackingThreshold, kp, speed):
    if junctionPort == 3:
        while leftSensor.reflection() > junctionThreshold:
            SinglePTrack(trackingPort, trackingThreshold, kp, speed)
    elif junctionPort == 2:
        while middleSensor.reflection() > junctionThreshold:
            SinglePTrack(trackingPort, trackingThreshold, kp, speed)
    else:
        while rightSensor.reflection() > junctionThreshold:
            SinglePTrack(trackingPort, trackingThreshold, kp, speed)
    leftMotor.stop()
    rightMotor.stop()


def SinglePTrackTillDegrees(degrees, trackingPort, trackingThreshold, kp, speed):
    leftMotor.reset_angle(0)
    while abs(leftMotor.angle()) < abs(degrees):
        SinglePTrack(trackingPort, trackingThreshold, kp, speed)
    leftMotor.stop()
    rightMotor.stop()


def WaitUntillPressed(text: str):
    while buttonSensor.pressed() == False:
        pass
    print(text)


def ev3Print(text: str):
    print(text)
    ev3.screen.set_font(big_font)
    ev3.screen.clear()
    ev3.screen.print(text)


def betterStalled(leftSpeed, rightSpeed):
    leftMotor.run(leftSpeed)
    rightMotor.run(rightSpeed)
    wait(2000)
    while True:
        if (abs(leftMotor.speed()) < abs(leftSpeed * 0.1)) or (abs(rightMotor.speed()) < abs(rightSpeed * 0.1)):
            leftMotor.stop()
            rightMotor.stop()
            break


def SinglePDTrack(sensorPort, threshold, kp, kd, speed):
    ref = rightSensor.reflection()
    global last_error  # im so smart
    error = ref - threshold
    p_gain = error * kp
    derivative = error - last_error
    d_gain = derivative * kd
    leftMotor.run(speed-(p_gain+d_gain))
    rightMotor.run(speed+(p_gain+d_gain))
    last_error = error


def SinglePDTrackDegrees(degrees, trackingPort, threshold, kp, kd, speed):
    leftMotor.reset_angle(0)
    while abs(leftMotor.angle()) < abs(degrees):
        SinglePDTrack(trackingPort, threshold, kp, kd, speed)
    leftMotor.hold()
    rightMotor.hold()


def SinglePDTrackTillJunction(junctionPort, junctionThreshold, trackingPort, trackingThreshold, kp, kd, speed):
    if junctionPort == 3:
        while leftSensor.reflection() > junctionThreshold:
            SinglePDTrack(trackingPort, trackingThreshold, kp, kd, speed)
    elif junctionPort == 2:
        while middleSensor.reflection() > junctionThreshold:
            SinglePDTrack(trackingPort, trackingThreshold, kp, kd, speed)
    else:
        while rightSensor.reflection() > junctionThreshold:
            SinglePDTrack(trackingPort, trackingThreshold, kp, kd, speed)
    leftMotor.hold()
    rightMotor.hold()

def startRun():
    leftMedMotor.stop()
    rightMedMotor.stop()
    WaitUntillPressed("1")
    leftMedMotor.hold()
    rightMedMotor.hold()

####### R E A L #### R U N ##########

