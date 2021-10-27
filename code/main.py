#!/usr/bin/env python3
import time

from ev3dev2.display import Display
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import Sensor, INPUT_1, UltrasonicSensor
from ev3dev2.port import LegoPort
