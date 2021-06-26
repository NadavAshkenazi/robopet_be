#!/usr/bin/python3
import time
import math
from datetime import datetime
from robopetSerial import mySerial
from robopetSounds import make_repetitive_sounds, Sound
from RobopetFaceDetect.main import getLocation
import threading

MIN_X_ANGLE = 0
MAX_X_ANGLE = 180
MIN_Y_ANGLE = 0
MAX_Y_ANGLE = 90
CAMERA_STEP = 10


def _bark():
    t = threading.Thread(target=make_repetitive_sounds, args=(Sound.BARK_TWICE, 2.5))
    t.start()
    time.sleep(0.5)
    for i in range(4):
        _bark_motion()
    t.join()


def _bark_motion():
    ser = mySerial()
    ser.init_serial()
    ser.write("mouth open")
    time.sleep(0.3)
    ser.write("mouth close")
    time.sleep(0.3)


def _spin():
    ser = mySerial()
    ser.init_serial()
    t = threading.Thread(target=make_repetitive_sounds, args=(Sound.HAPPY_BARK, 3.5))
    t.start()
    ser.write("mouth open")
    time.sleep(2)
    ser.write("cam_setX 170")
    time.sleep(2)
    ser.write("tail --start 60")
    time.sleep(2)
    ser.write("tail --end 10")
    time.sleep(2)
    ser.write("spin --left --front 12")
    time.sleep(4)
    ser.write("mouth close")
    time.sleep(3)
    t.join()


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
    turn = math.floor(60*(1 + location[0]))
    print(f"turn is {turn}")
    ser = mySerial()
    ser.init_serial()
    ser.write(f"turn {turn}")
    ser.write("forward")
    time.sleep(2)
    ser.write("stop")
    ser.write("turn 90")


def behave_hostile():
    ser = mySerial()
    ser.init_serial()
    while True:
        ser.write("turn 120")
        time.sleep(1)
        ser.write("turn 60")
        time.sleep(1)


def behave_friendly():
    ser = mySerial()
    ser.init_serial()
    ser.write("eyes green")
    # _spin()
    location = search_face()
    # if location is None:
    #     ser.write("spin --left --front 2")
    #     location = search_face()
    if location is None:
        _bark()
        return
    align_by_location(location)
