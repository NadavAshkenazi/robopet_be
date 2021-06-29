from robopetSerial import mySerial

if __name__ == "__main__":
    ser = mySerial()
    ser.init_serial()
    ser.write("stop")