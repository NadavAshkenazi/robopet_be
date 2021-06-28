#!/usr/bin/python3

from robopetSerial import mySerial
from time import sleep

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

        if 10 < angle < 170:
            angle_x -= STEP
        elif 190 < angle < 350:
            angle_x += STEP

        if angle > 280 or angle < 80:
            angle_y += STEP
        else:
            angle_y -= STEP

        ser.write(f"cam_setX {angle_x}")
        ser.write(f"cam_setY {angle_y}")
        sleep(DELAY)


if __name__ == "__main__":
    ser = mySerial()
    ser.init_serial()
    # ser.write(b"DEBUG ON#")
    # read_serial(ser)
    manual_movement(ser)
