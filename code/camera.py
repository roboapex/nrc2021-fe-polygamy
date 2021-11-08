#!/usr/bin/env python3
import time
from ev3dev2.sensor import Sensor, INPUT_4
from ev3dev2.port import LegoPort

from smbus import SMBus

# Set LEGO port for Pixy2 on input port 4
in1 = LegoPort(INPUT_4)
in1.mode = "other-i2c"
# Short wait for port to get ready
time.sleep(0.5)

# Settings for I2C (SMBus(6)) for INPUT_4
bus = SMBus(6)
address = 0x54

data = [174, 193, 14, 0]
bus.write_i2c_block_data(address, 0, data)
block = bus.read_i2c_block_data(address, 0, 13)
print("Firmware version: {}.{}\n".format(str(block[8]), str(block[9])))

traffic = []

# Sigmap 1 is trained on red
# Sigmap 2 is trained on green


def colour(sigmap):
    sigmap = int(sigmap)
    data = [174, 193, 32, 2, sigmap, 1]
    bus.write_i2c_block_data(address, 0, data)
    block = bus.read_i2c_block_data(address, 0, 20)

    time.sleep(0.1)

    if (block[7] * 256 + block[6]) == sigmap:
        x = block[9] * 256 + block[8]
        w = block[13] * 256 + block[12]
        h = block[15] * 256 + block[14]
        traffic.append([w * h, x])

    return traffic