#!/usr/bin/env python3
from time import sleep

"""
from ev3dev2.display import Display
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
"""
from ev3dev2.sensor import Sensor, INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.port import LegoPort
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_D, OUTPUT_B, MediumMotor

from smbus import SMBus

# Set LEGO port for Pixy2 on input port 4
in1 = LegoPort(INPUT_4)
in1.mode = "auto"
# Short wait for port to get ready
sleep(0.5)

# Settings for I2C (SMBus(6)) for INPUT_4
bus = SMBus(6)
address = 0x54
data = [174, 193, 14, 0]
"""
bus.write_i2c_block_data(address, 0, data)
block = bus.read_i2c_block_data(address, 0, 13)

print("Firmware version: {}.{}\n".format(str(block[8]), str(block[9])))
"""
# frontUltra = UltrasonicSensor(INPUT_1)
leftUltra = UltrasonicSensor(INPUT_2)
rightUltra = UltrasonicSensor(INPUT_3)