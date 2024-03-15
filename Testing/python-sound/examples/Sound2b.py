# Sound2b.py

from soundplayer import SoundPlayer
import time

# Sine of 1000 Hz during 5 s, non-blocking, device 1
SoundPlayer.playTone(1000, 5, False, 1)
n = 0
while SoundPlayer.isPlaying():
   print "playing #", n
   time.sleep(1)
   n += 1
print "done"
    
