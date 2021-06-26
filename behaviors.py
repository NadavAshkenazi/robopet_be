#!/usr/bin/python3
import time
from datetime import datetime
from robopetSerial import mySerial
from robopet_flask_be import _spin, _bark
from RobopetFaceDetect.main import getLocation
import threading

MIN_X_ANGLE = 0
MAX_X_ANGLE = 180
MIN_Y_ANGLE = 0
MAX_Y_ANGLE = 90
CAMERA_STEP = 10

def search_face():
    ser = mySerial()
    ser.init_serial()
    location = None
    for y in range(MAX_Y_ANGLE, MIN_Y_ANGLE, -1*CAMERA_STEP):
        if location is not None:
            break
        ser.write(f"cam_setY {y}")
        for x in range(MIN_X_ANGLE, MAX_X_ANGLE, CAMERA_STEP):
            ser.write(f"cam_setX {x}")
            location = getLocation(10)
            if location is not None:
                break

    return location

def move_by_location(location):
    pass


def align_by_location(location):
    turn = 60*(1 + location[0])
    ser = mySerial()
    ser.init_serial()
    ser.write(f"turn {turn}")
    time.sleep(0.3)
    ser.write("turn 90")


def hostile():
    ser = mySerial()
    ser.init_serial()
    while True:
        ser.write("turn 120")
        time.sleep(1)
        ser.write("turn 60")
        time.sleep(1)


def friendly():
    ser = mySerial()
    ser.init_serial()
    ser.write("eyes green")
    _spin()
    location = search_face()
    if location is None:
        ser.write("spin --left --front 2")
        location = search_face()
    if location is None:
        _bark()
        return
    align_by_location(location)
