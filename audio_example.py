import time
from pygame import mixer

mixer.init()
mixer.music.load("sounds/bark1.wav")
mixer.music.set_volume(1.0)

while True:
    if not mixer.music.get_busy():
        mixer.music.play()
        time.sleep(0.5)
