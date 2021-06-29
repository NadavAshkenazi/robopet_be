#!/usr/bin/python3

from robopetSerial import mySerial
from time import sleep
from math import sin, cos, radians

STEP = 20
DELAY = 0.01

def read_serial(ser):
    try:
        while ser.in_waiting:
            line = ser.read()
            print(line)
    except:
        pass

# True = forwards, False = backwards
def manual_movement(ser):
    angle_x = 90
    angle_y = 45
    ser.write("camera_setX 90")
    ser.write("camera_setY 45")

    while True:
        angle = int(input())
        if angle == 0:
            continue

        cos_angle = (cos(radians(angle)) + 1) * 45
        if cos_angle == 90:
            cos_angle = 88
        elif cos_angle == 0:
            cos_angle = 2

        sin_angle = (sin(radians(angle)) + 1) * 90
        if sin_angle == 180:
            sin_angle = 178
        elif sin_angle == 0:
            sin_angle = 2


        # if 10 < angle < 170:
        #     angle_x -= STEP
        # elif 190 < angle < 350:
        #     angle_x += STEP
        #
        # if angle > 280 or angle < 80:
        #     angle_y += STEP
        # else:
        #     angle_y -= STEP

        ser.write(f"cam_setX {sin_angle}")
        ser.write(f"cam_setY {cos_angle}")
        sleep(DELAY)


if __name__ == "__main__":
    ser = mySerial()
    ser.init_serial()
    # ser.write(b"DEBUG ON#")
    # read_serial(ser)
    manual_movement(ser)
