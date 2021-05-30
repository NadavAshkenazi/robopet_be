#!/usr/bin/python3

from enum import Enum
import serial
import time

delay = 0.2
class Direction(Enum):
    FORWARDS = 1
    BACKWARDS = 2
    STOPPED = 3

def read_serial(ser):
    try:
        for i in range(5):
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
    except:
        pass

# True = forwards, False = backwards
def manual_movement(ser):
    direction = Direction.STOPPED
    # set speed in the beginning I think

    while True:
        time.sleep(delay)
        angle = int(input())
        if angle == 0:
            ser.write(b"stop")
            direction = Direction.STOPPED
            continue

        if angle > 0 and direction != Direction.FORWARDS:
            direction = Direction.FORWARDS
            ser.write(b"forward")
            read_serial(ser)
        elif angle < 0 and direction != Direction.BACKWARDS:
            direction = Direction.BACKWARDS
            ser.write(b"backward")
            read_serial(ser)
        angle = abs(angle)
        time.sleep(delay)
        ser.write(b"turn %d" % angle)
        read_serial(ser)
        time.sleep(delay)
        ser.write(b"speed 200")
        read_serial(ser)

if __name__ == "__main__":
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    time.sleep(delay)
    ser.write(b"speed 200")
    read_serial(ser)
    time.sleep(delay)
    ser.write(b"forward")
    read_serial(ser)
    time.sleep(delay)
    manual_movement(ser)
