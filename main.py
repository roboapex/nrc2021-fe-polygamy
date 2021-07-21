#!/usr/bin/env pybricks-micropython
import time

from pybricks.ev3devices import (ColorSensor, GyroSensor, InfraredSensor,
                                 Motor, TouchSensor, UltrasonicSensor)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import Font, ImageFile, SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait
from ev3dev2.display import Display

# Import smbus drivers for i2c camera
from smbus import SMBus

from ev3dev2.port import LegoPort
from ev3dev2.sensor import INPUT_4

# Set LEGO port for Pixy2 on input port 1
in1 = LegoPort(INPUT_4)
in1.mode = 'other-i2c'
# Short wait for the port to get ready
time.sleep(0.5)

 # Settings for I2C (SMBus(3) for INPUT_1)
bus = SMBus(6)
address = 0x54

# Request and read protocal for camera
data = [174, 193, 32, 2, 1, 1]

while True:
    bus.write_i2c_block_data(address, 0, data)
    block = bus.read_i2c_block_data(address, 0, 20)
    sig = block[7]*256 + block[6]
    x = block[9]*256 + block[8]
    y = block[11]*256 + block[10]
    w = block[13]*256 + block[12]
    h = block[15]*256 + block[14]
    print("sig: {} | x: {} | y: {} | w: {} | h: {}".format(sig,x,y,w,h))

