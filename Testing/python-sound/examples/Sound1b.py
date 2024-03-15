# Sound1b.py

from soundplayer import SoundPlayer
import time
    
# Use device with ID 0  (mostly standard audio output)
# Sound resource in current folder
p = SoundPlayer("salza1.wav", 1)        
print "play for 10 s"
p.play() # non blocking, volume = 1
n = 0
while True:
    if not p.isPlaying():
       break
    print "playing:", n
    if n == 10:
        p.stop()
        print "stopped"
    n += 1
    time.sleep(1)
print "done"
    
