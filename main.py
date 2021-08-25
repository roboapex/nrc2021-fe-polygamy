#!/usr/bin/env python3
import time

from ev3dev2.display import Display
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import Sensor, INPUT_1, UltrasonicSensor
from ev3dev2.port import LegoPort

# Set LEGO port for Pixy2 on input port 1
in1 = LegoPort(INPUT_1)
in1.mode = 'other-i2c'
# Short wait for the port to get ready
time.sleep(0.5)

 # Settings for I2C (SMBus(3) for INPUT_1)
bus = SMBus(3)
address = 0x54

# Request and read protocal for camera
data = [174, 193, 32, 2, 1, 1]
counter = 0