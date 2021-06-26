import time
import serial
import glob

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class mySerial(metaclass=Singleton, ):
    ser = None
    def init_serial(self):
        if self.ser is None:
            self.ser = serial.Serial(glob.glob("/dev/ttyACM*")[0], 9600, timeout=1)
            self.ser.flush()

    def read(self):
        try:
            while self.ser.in_waiting:
                line = self.ser.readline().decode('utf-8').rstrip()
                print(line)
            return line
        except:
            pass

    def write(self, cmd):
        self.ser.reset_input_buffer()
        self.ser.write(bytes(cmd+"#", "UTF-8"))

    def flush_input(self):
        self.ser.reset_input_buffer()
        

