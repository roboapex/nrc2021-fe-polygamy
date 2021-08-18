#!/usr/bin/env python3
import time

from ev3dev2.display import Display
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import Sensor, INPUT_1, UltrasonicSensor
from ev3dev2.port import LegoPort
from smbus import SMBus

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

UltrasonicSensor.distance_centimeters()

while True:
    counter += 1
    bus.write_i2c_block_data(address, 0, data)
    block = bus.read_i2c_block_data(address, 0, 20)
    print(block, block[19])
    time.sleep(0.1)
    '''
    sig = block[7]*256 + block[6]
    x = block[9]*256 + block[8]
    y = block[11]*256 + block[10]
    w = block[13]*256 + block[12]
    h = block[15]*256 + block[14]
    '''
    #print("sig: {} | x: {} | y: {} | w: {} | h: {}".format(sig, x, y, w, h))

