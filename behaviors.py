#!/usr/bin/python3
import time
import math
from datetime import datetime
from robopetSerial import mySerial
from robopetSounds import make_repetitive_sounds, Soundtrack, make_sound, stop_sound
from RobopetFaceDetect.main import getLocation, getLocationHostile
from arduinoInfra import turn_30_right, turn_30_left
import threading
from multiprocessing import Process
from pygame import mixer

MIN_X_ANGLE = 0
MAX_X_ANGLE = 180
MIN_Y_ANGLE = 0
MAX_Y_ANGLE = 90
CAMERA_STEP = 20


def _bark(sound=Soundtrack.BARK_TWICE, time=2.5):
    # t = threading.Thread(target=make_repetitive_sounds, args=(sound, time))
    # t.start()
    make_sound(sound, 0)
    time.sleep(0.5)
    for i in range(4):
        _bark_motion()
    stop_sound(0)


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
    t = threading.Thread(target=make_repetitive_sounds, args=(Soundtrack.HAPPY_BARK, 3.5))
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
    location, id, confidence = getLocationHostile(3)
    print("Found stranger")
    print(location)
    return id, confidence


def search_face():
    ser = mySerial()
    ser.init_serial()
    print("sleeping before cam_setY 90")
    time.sleep(2)
    ser.write("cam_setY 75")
    ser.write("cam_setX 90")
    location = getLocation(3)
    if location is not None and 0.3 < location[0] < 0.7:
        print("Found at 90")
        print(location)
        return location, 90

    for x in range(MIN_X_ANGLE, MAX_X_ANGLE, CAMERA_STEP):
        print(f"cam_setX {x}")
        ser.write(f"cam_setX {x}")
        location = getLocation(3)
        if location is not None and 0.3 < location[0] < 0.7:
            print(f"Found at {x}")
            print(location)
            return location, x

    return None


def move_until_obstacle(location):
    ser = mySerial()
    ser.init_serial()

    ser.write("speed 200")
    ser.flush_input()
    while True:
        ser.write("dist --front")
        dist = None
        while dist is None or not dist.isnumeric():
            dist = ser.read()
        dist = float(dist)
        if 40 > dist > 0:
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
    ser.write("mouthSet 60")
    make_sound(Soundtrack.GROWL, 0)
    location = search_face()
    if location is None:
        stop_sound(0)
        _bark()
        return

    align_by_location(location)
    id, confidence = search_face_hostile()
    print(f"id is {id}")
    print(f"confidence is {confidence}")
    stop_sound(0)
    if id <= 0 or confidence > 100:
        _bark(Soundtrack.SCARY_BARK, 5)
        ser.write("eyes red")
        for i in range(3):
            ser.write("forward")
            time.sleep(0.5)
            ser.write("backward")
            time.sleep(0.5)
        ser.write("stop")
    else:
        _bark(Soundtrack.HAPPY_BARK, 5)
        ser.write("eyes green")
        ser.write("shakeTail")
        time.sleep(1)
        ser.write("shakeTail")


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
