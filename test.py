#!/usr/bin/python3

from enum import Enum

class Direction(Enum):
    FORWARDS = 1
    BACKWARDS = 2
    STOPPED = 3

# True = forwards, False = backwards
def manual_movement():
    direction = Direction.STOPPED
    # set speed in the beginning I think

    while True:
        # TODO: switch prints with serial prints
        angle = int(input())
        if angle == 0:
            print("stop")
            direction = Direction.STOPPED
            continue

        if angle > 0 and direction != Direction.FORWARDS:
            direction = Direction.FORWARDS
            print("forward")
        elif angle < 0 and direction != Direction.BACKWARDS:
            direction = Direction.BACKWARDS
            print("backward")
        print(angle)

manual_movement()
