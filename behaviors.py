#!/usr/bin/python3
import time
from datetime import datetime
from robopetSerial import mySerial


def dummy_hostile():
    ser = mySerial()
    ser.init_serial()
    while True:
        ser.write("turn 120")
        time.sleep(1)
        ser.write("turn 60")
        time.sleep(1)


def dummy_friendly():
    ser = mySerial()
    ser.init_serial()
    while True:
        ser.write("cam_setX 0")
        time.sleep(1)
        ser.write("cam_setX 90")
        time.sleep(1)


def dummy_follow():
    while True:
        with open('follow', 'a+') as f:
            f.write(datetime.now().strftime("%H:%M:%S") + "\n")
            f.flush()
        time.sleep(0.5)
