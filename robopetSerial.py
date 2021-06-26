import time
import serial
import os

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class mySerial(metaclass=Singleton):
    ser = None
    def init_serial(self):
        if self.ser is None:
            self.ser = serial.Serial(os.getenv('arduino_dev'), 9600, timeout=1)
            self.ser.flush()

    def read(self):
        try:
            while self.ser.in_waiting:
                line = self.ser.readline().decode('utf-8').rstrip()
                print(line)
        except:
            pass

    def write(self, cmd):
        self.ser.write(bytes(cmd+"#", "UTF-8"))