#!/usr/bin/python3

from enum import Enum
from robopetSerial import mySerial
import time

delay = 0


class Direction(Enum):
    FORWARDS = 1
    BACKWARDS = 2
    STOPPED = 3


class Orientation(Enum):
    STRAIGHT = 90
    LEFT = 60
    RIGHT = 120


def read_serial(ser):
    try:
        time.sleep(delay)
        while ser.in_waiting:
            line = ser.read()
            print(line)
    except:
        pass


def get_orientation(angle):
    if 60 <= angle < 80:
        orientation = Orientation.LEFT
    elif 80 <= angle < 100:
        orientation = Orientation.STRAIGHT
    else:
        orientation = Orientation.RIGHT

    return orientation


# True = forwards, False = backwards
def manual_movement(ser):
    direction = Direction.STOPPED
    orientation = Orientation.STRAIGHT

    while True:
        inp = input()
        if inp == "stop":
            ser.write("stop")
            direction = Direction.STOPPED
            read_serial(ser)
            continue

        angle = int(inp)
        if angle > 0 and direction != Direction.FORWARDS:
            direction = Direction.FORWARDS
            ser.write("speed 200")
            read_serial(ser)
            ser.write("forward")
            read_serial(ser)
        elif angle < 0 and direction != Direction.BACKWARDS:
            direction = Direction.BACKWARDS
            ser.write("speed 200")
            read_serial(ser)
            ser.write("backward")
            read_serial(ser)
        next_orientation = get_orientation(abs(angle))
        if next_orientation != orientation:
            orientation = next_orientation
            ser.write("turn %d" % orientation.value)
            read_serial(ser)


if __name__ == "__main__":
    ser = mySerial()
    ser.init_serial()
    # ser.write(b"DEBUG ON#")
    # read_serial(ser)
    manual_movement(ser)
