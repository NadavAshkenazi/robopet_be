#!/usr/bin/python3
import time
import math
from datetime import datetime
from robopetSerial import mySerial
from robopetSounds import make_repetitive_sounds, Sound
from RobopetFaceDetect.main import getLocation
from arduinoInfra import turn_30_right, turn_30_left
import threading
from multiprocessing import Process

MIN_X_ANGLE = 0
MAX_X_ANGLE = 180
MIN_Y_ANGLE = 0
MAX_Y_ANGLE = 90
CAMERA_STEP = 20


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


def search_face_hostile():
    ser = mySerial()
    ser.init_serial()
    print("sleeping before cam_setY 75")
    time.sleep(2)
    ser.write("cam_setY 75")
    ser.write("cam_setX 90")
    location = getLocationHostile(3)
    if location is not None:
        print("Found stranger")
        print(location)
        return location, 90

    return None


def search_face():
    ser = mySerial()
    ser.init_serial()
    print("sleeping before cam_setY 90")
    time.sleep(2)
    ser.write("cam_setY 75")
    ser.write("cam_setX 90")
    location = getLocation(3)
    if location is not None and location[0] > 0.3 and location[0] < 0.7:
        print("Found at 90")
        print(location)
        return location, 90

    for x in range(MIN_X_ANGLE, MAX_X_ANGLE, CAMERA_STEP):
        print(f"cam_setX {x}")
        ser.write(f"cam_setX {x}")
        location = getLocation(3)
        if location is not None and location[0] > 0.3 and location[0] < 0.7:
            print(f"Found at {x}")
            print(location)
            return location, x

    return None


def move_until_obstacle(location):
    ser.write("speed 200")
    ser.flush_input()
    while True:
        ser.write("dist --front")
        dist = None
        while dist is None or not dist.isnumeric():
            dist = ser.read()
        dist = float(dist)
        if (dist < 40 and dist > 0):
            break
    ser.write("stop")


def align_by_location(location):
    # turn = math.floor(60*(1 + location[0]))
    turn = 180 - location[1]
    actual_turn = turn - 90
    print(f"turn is {turn}")
    if actual_turn > 0:
        times = actual_turn // 30
        for i in range(times):
            turn_30_right()
    else:
        times = -1*actual_turn // 30
        for i in range(times):
            turn_30_left()
    ser = mySerial()
    ser.init_serial()
    ser.write("turn 90")
    ser.write("cam_setX 90")


def behave_hostile():
    ser = mySerial()
    ser.init_serial()
    ser.write("eyes red")
    p = Process(target=make_repetitive_sounds, args=(Sound.GROWL, 30))
    location = search_face()
    if location is None:
        _bark()
        return

    align_by_location(location)
    res = search_face_hostile()
    if p.is_alive():
        p.terminate()
    if res is not None:
        t = threading.Thread(target=make_repetitive_sounds, args=(Sound.MEDIUM_ANGRY_BARK, 5))
        t.start()
        for i in range(3):
            ser.write("forward")
            time.sleep(0.5)
            ser.write("backward")
        ser.write("stop")
    else:
        t = threading.Thread(target=make_repetitive_sounds, args=(Sound.MEDIUM_ANGRY_BARK, 5))
        t.start()
        ser.write("eyes green")
        ser.write("shakeTail")
        time.sleep(1)
        ser.write("shakeTail")
    t.join()


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
    move_until_obstacle()
