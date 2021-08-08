#!/usr/bin/python3
import time
import math
from datetime import datetime
from robopetSerial import mySerial
from robopetSounds import make_repetitive_sounds, Soundtrack, make_sound, stop_sound
# from RobopetFaceDetect.main import getLocation, getLocationHostile, face_recognize
from RobopetFaceDetect.Detection.detection import FaceDetector
from RobopetFaceDetect.Recognition.recognition import FaceRecogniser
from arduinoInfra import turn_30_right, turn_30_left
import threading
from multiprocessing import Process
from pygame import mixer

MIN_X_ANGLE = 0
MAX_X_ANGLE = 180
MIN_Y_ANGLE = 0
MAX_Y_ANGLE = 90
CAMERA_STEP = 20


def _bark(sound=Soundtrack.BARK_TWICE):
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
    time.sleep(0.5)
    ser.write("cam_setX 170")
    time.sleep(0.5)
    ser.write("tail --end 15")
    time.sleep(0.5)
    ser.write("spin --left --front 12")
    time.sleep(0.5)
    ser.write("tail --end 90")
    time.sleep(0.5)
    ser.write("cam_setX 90")
    time.sleep(4)
    ser.write("mouth close")
    time.sleep(3)
    t.join()


def recognize_owner():
    recogniser = FaceRecogniser()
    recogniser.load_embeddings()
    ser = mySerial()
    ser.init_serial()
    print("sleeping before cam_setY 75")
    time.sleep(2)
    ser.write("cam_setY 75")
    ser.write("cam_setX 90")
    name = recogniser.rec_video_from_camera()
    print("Found person")
    return name


# def search_owner():
#     print("Search owner")
#     ser = mySerial()
#     ser.init_serial()
#     print("cam_setY 75")
#     time.sleep(2)
#     ser.write("cam_setY 75")
#     ser.write("cam_setX 90")
#     location, id, confidence = getLocationHostile(6)
#     if id <= 0 or confidence >= 100:
#         return None

#     if location is not None and 0.3 < location[0] < 0.7:
#         print("Found at 90")
#         print(location)
#         return location, 90

#     for x in range(MIN_X_ANGLE, MAX_X_ANGLE, CAMERA_STEP):
#         print(f"cam_setX {x}")
#         ser.write(f"cam_setX {x}")
#         location, id, confidence = getLocationHostile(6)
#         if id <= 0 or confidence >= 100:
#             return None

#         if location is not None and 0.3 < location[0] < 0.7:
#             print(f"Found at {x}")
#             print(location)
#             return location, x

#     return None


def search_face():
    """
    returns (location, head_angle)
    location is a tuple of x,y axis in the frame
    returns None if no faces were found
    """
    ser = mySerial()
    ser.init_serial()
    detector = FaceDetector()
    time.sleep(1)
    ser.write("cam_setX 90")
    ser.write("cam_setY 75")
    location = detector.get_face_location(3)
    if location is not None and 0.3 < location[0] < 0.7:
        print("Found at 90")
        print(location)
        return location, 90

    for x in range(MIN_X_ANGLE, MAX_X_ANGLE, CAMERA_STEP):
        ser.write("cam_setY 75")
        time.sleep(0.1)
        print(f"cam_setX {x}")
        ser.write(f"cam_setX {x}")
        location = detector.get_face_location(3)
        if location is not None and 0.3 < location[0] < 0.7:
            print(f"Found at {x}")
            print(location)
            return location, x

    return None, None


def move_until_obstacle():
    ser = mySerial()
    ser.init_serial()

    stop = False
    while not stop:
        ser.write("speed 170")
        ser.write("forward")
        ser.write("turn 90")
        time.sleep(0.2)
        ser.write("stop")
        dist = None
        while dist is None or not dist.isnumeric():
            ser.write("dist --front")
            time.sleep(0.2)
            dist = ser.read()

        dist = float(dist)
        if 40 > dist > 0:
            stop = True

    print("Stopping")
    ser.write("stop")


def align_by_location(location):
    print(f"align by location: {location}")
    actual_turn = location - 90
    print(f"turn is {location}")
    if actual_turn > 0:
        times = actual_turn // 30
        for i in range(times):
            turn_30_right()
        turn_30_left()
    else:
        times = -1*actual_turn // 30
        for i in range(times):
            turn_30_left()
        turn_30_right()
    # ser = mySerial()
    # ser.init_serial()
    # ser.write("turn 90")
    # ser.write("cam_setX 90")


def behave_hostile():
    print("Hostile start")
    ser = mySerial()
    ser.init_serial()
    ser.write("mouthSet 60")
    make_sound(Soundtrack.GROWL, 0)
    location_on_frame, head_angle = search_face()
    if location_on_frame is None:
        stop_sound(0)
        _bark()
        return

    align_by_location(180 - head_angle)
    print("starting search_face_hostile")
    name = recognize_owner()
    stop_sound(0)
    if name == "Unknown":
        print("Stranger")
        make_sound(Soundtrack.SCARY_BARK, 0)
        ser.write("eyes red")
        for i in range(3):
            ser.write("forward")
            ser.write("turn 90")
            time.sleep(0.5)
            ser.write("backward")
            time.sleep(1)
        ser.write("stop")
    else:
        print("Owner")
        make_sound(Soundtrack.HAPPY_BARK, 0)
        ser.write("eyes green")
        ser.write("shakeTail")
        ser.write("shakeTail")
    stop_sound(0)


def behave_friendly():
    ser = mySerial()
    ser.init_serial()
    time.sleep(0.1)
    ser.write("eyes green")
    time.sleep(0.1)
    ser.write("turn 90")
    # _spin()
    location_on_frame, head_angle = search_face()
    # if location is None:
    #     ser.write("spin --left --front 2")
    #     location = search_face()
    if location_on_frame is None:
        _bark()
        return
    align_by_location(180 - head_angle)
    ser.write("turn 90")
    ser.write("cam_setX 90")
    move_until_obstacle()
    ser.write("shakeTail")


# def follow_face():
#     ser = mySerial()
#     ser.init_serial()
#     ser.write("speed 200")
# 
#     dist = 100
#     while 40 < dist and dist != 0:
#         ser.write("forward")
#         time.sleep(1)
#         ser.write("stop")
#         ser.write("dist --front")
#         dist = None
#         while dist is None or not dist.isnumeric():
#             dist = ser.read()
#         dist = float(dist)
# 
#         location = getLocation(2)
#         if 40 < dist and dist != 0:
#             if location is None:
#                 continue
#             if location[0] < 0.3:
#                 print("Triggered < 0.3")
#                 align_by_location(60)
#             elif location[0] > 0.7:
#                 print("Triggered > 0.7")
#                 align_by_location(120)
#         else:
#             break
# 
#     ser.write("stop")
# 
# 
# def behave_follow():
#     ser = mySerial()
#     ser.init_serial()
#     location = search_face()
#     if location is None:
#         _bark()
#         return
#     align_by_location(180 - location[1])
#     ser.write("eyes blue")
#     follow_face()
