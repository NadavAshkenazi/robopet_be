import robopetSerial
import time
from enum import Enum
from pygame import mixer
from robopetSerial import mySerial


class Soundtrack(Enum):
    BARK_TWICE = 1
    HAPPY_BARK = 2
    MEDIUM_ANGRY_BARK = 3
    SCARY_BARK = 4
    GROWL = 5


sound_files = {
    Soundtrack.BARK_TWICE: "sounds/bark_once.wav",
    Soundtrack.HAPPY_BARK: "sounds/happy_barks.wav",
    Soundtrack.MEDIUM_ANGRY_BARK: "sounds/medium_angry_bark.wav",
    Soundtrack.SCARY_BARK: "sounds/scary_bark.wav",
    Soundtrack.GROWL: "sounds/dog-growling.wav"
}

sound_objects = {k: mixer.Sound(v) for k, v in sound_files.items()}

sound_lengths = {
    Soundtrack.BARK_TWICE: 0.25,
    Soundtrack.HAPPY_BARK: 6,
    Soundtrack.MEDIUM_ANGRY_BARK: 2,
    Soundtrack.SCARY_BARK: 2,
    Soundtrack.GROWL: 6
}


def stop_sound(channel):
    mixer.init()
    mixer.Channel(channel).stop()


def make_sound(sound, channel, loops=-1):
    mixer.init()
    c = mixer.Channel(channel)
    c.play(sound_objects[sound], loops=loops)


def make_repetitive_sounds(sound, duration):
    """
    :param sound: what sound to make, instance of Sound
    :param duration: duration in seconds
    :return: void
    """
    start = time.time()
    make_sound(sound, 0)
    while time.time() - start < duration:
        pass

    stop_sound(0)


if __name__ == "__main__":
    make_repetitive_sounds(Soundtrack.SCARY_BARK, 5)
