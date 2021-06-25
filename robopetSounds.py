import robopetSerial
import time
from enum import Enum
from pygame import mixer

from robopetSerial import mySerial


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
