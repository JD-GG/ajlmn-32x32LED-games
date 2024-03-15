# Sound2b.py

from soundplayer import SoundPlayer

# Sine tone during 0.1 s, blocking, device 0
dev = 0
SoundPlayer.playTone(900, 0.1, True, dev) # 900 Hz
SoundPlayer.playTone(800, 0.1, True, dev) # 600 Hz
SoundPlayer.playTone(600, 0.1, True, dev) # 600 Hz
print "done"
    
