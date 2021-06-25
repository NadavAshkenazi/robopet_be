#!/usr/bin/python3

from enum import Enum
import robopetSerial
import time

delay = 0
class Direction(Enum):
    FORWARDS = 1
    BACKWARDS = 2
    STOPPED = 3

def read_serial(ser):
    try:
        time.sleep(delay)
        while ser.in_waiting:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
    except:
        pass

# True = forwards, False = backwards
def manual_movement(ser):
    direction = Direction.STOPPED

    while True:
        angle = int(input())
        read_serial(ser)
        if angle == 0:
            ser.write(b"stop#")
            direction = Direction.STOPPED
            read_serial(ser)
            continue

        if angle > 0 and direction != Direction.FORWARDS:
            direction = Direction.FORWARDS
            ser.write(b"speed 200#")
            read_serial(ser)
            ser.write(b"forward#")
            read_serial(ser)
        elif angle < 0 and direction != Direction.BACKWARDS:
            direction = Direction.BACKWARDS
            ser.write(b"speed 200#")
            read_serial(ser)
            ser.write(b"backward#")
            read_serial(ser)
        angle = abs(angle)
        ser.write(b"turn %d#" % angle)
        read_serial(ser)

if __name__ == "__main__":
    ser = robopetSerial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    # ser.write(b"DEBUG ON#")
    # read_serial(ser)
    manual_movement(ser)
