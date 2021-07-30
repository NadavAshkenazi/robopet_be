from robopetSerial import mySerial
from time import sleep


def turn_30_right(times=1):
    ser = mySerial()
    ser.init_serial()

    ser.write("speed 255")
    ser.write("forward")
    ser.write("right")
    sleep(0.4*times)
    ser.write("stop")

def turn_30_left(times=1):
    ser = mySerial()
    ser.init_serial()

    ser.write("speed 255")
    ser.write("forward")
    ser.write("left")
    sleep(0.4*times)
    ser.write("stop")
