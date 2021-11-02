#!/usr/bin/env python3
from time import sleep
from ev3dev2.sensor import Sensor, INPUT_4

from ev3dev2.port import LegoPort
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, OUTPUT_B, MediumMotor

from smbus import SMBus

# Set LEGO port for Pixy2 on input port 4
in1 = LegoPort(INPUT_4)
in1.mode = "other-i2c"
# Short wait for port to get ready
sleep(0.5)

# Settings for I2C (SMBus(6)) for INPUT_4
bus = SMBus(6)
address = 0x54
data = [174, 193, 14, 0]

bus.write_i2c_block_data(address, 0, data)
block = bus.read_i2c_block_data(address, 0, 13)

print("Firmware version: {}.{}\n".format(str(block[8]), str(block[9])))

frontUltra = UltrasonicSensor(INPUT_1)
leftUltra = UltrasonicSensor(INPUT_2)
rightUltra = UltrasonicSensor(INPUT_3)

counter = 0

frontUltra.Distance - Centimeters


def colour():
    counter += 1
    bus.write_i2c_block_data(address, 0, data)
    block = bus.read_i2c_block_data(address, 0, 20)
    print(block, block[19])
    time.sleep(0.1)
    """
    sig = block[7]*256 + block[6]
    x = block[9]*256 + block[8]
    y = block[11]*256 + block[10]
    w = block[13]*256 + block[12]
    h = block[15]*256 + block[14]
    """
    # print("sig: {} | x: {} | y: {} | w: {} | h: {}".format(sig, x, y, w, h))
