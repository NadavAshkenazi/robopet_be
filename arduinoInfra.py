from robopetSerial import mySerial
from time import sleep


def turn_30_right(times=1):
    ser = mySerial()
    ser.init_serial()

    ser.write("speed 255")
    ser.write("right")
    ser.write("forward")
    sleep(0.8*times)
    ser.write("stop")

def turn_30_left(times=1):
    ser = mySerial()
    ser.init_serial()

    ser.write("speed 255")
    ser.write("left")
    ser.write("forward")
    sleep(0.8*times)
    ser.write("stop")
