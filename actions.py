import serial
import time
import json
from enum import Enum
from RobopetFaceDetect.main import face_recognize
from pygame import mixer


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
            self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
            self.ser.flush()
    
    def read(self):
        try:
            time.sleep(delay)
            while self.ser.in_waiting:
                line = self.ser.readline().decode('utf-8').rstrip()
                print(line)
        except:
            pass
    
    def write(self, cmd):
        self.ser.write(bytes(cmd+"#", "UTF-8"))


class Sound(Enum):
    BARK_TWICE = 1
    HAPPY_BARK = 2
    MEDIUM_ANGRY_BARK = 3
    SCARY_BARK = 4


sound_files = {
    Sound.BARK_TWICE: "sounds/barking_twice.wav",
    Sound.HAPPY_BARK: "sounds/happy_barks.wav",
    Sound.MEDIUM_ANGRY_BARK: "sounds/medium_angry_bark.wav",
    Sound.SCARY_BARK: "sounds/scary_bark.wav"
}

sound_lengths = {
    Sound.BARK_TWICE: 2,
    Sound.HAPPY_BARK: 6,
    Sound.MEDIUM_ANGRY_BARK: 2,
    Sound.SCARY_BARK: 2
}


def init_serial():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    return ser


def send_serial_cmd(cmd):
    ser = mySerial()
    ser.init_serial()
    ser.write(cmd)
    

def make_sounds(sound):
    """
    make the dog bark
    :param sound: enum of type Sound
    :return: True iff sound was played
    """
    mixer.init()
    mixer.music.load(sound_files[sound])
    mixer.music.set_volume(1.0)
    if not mixer.music.get_busy():
        mixer.music.play()
        time.sleep(sound_lengths[sound])
        return True
    else:
        return False


def make_repetitive_sounds(sound, duration):
    """
    :param sound: what sound to make, instance of Sound
    :param duration: duration in seconds
    :return: void
    """
    start = time.time()
    while time.time() - start < duration:
        if make_sounds(sound):
            time.sleep(0.5)


if __name__ == "__main__":
    make_repetitive_sounds(Sound.SCARY_BARK, 10)
