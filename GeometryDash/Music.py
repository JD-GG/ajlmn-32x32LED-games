#pcm.!default {type hw card 1}
#ctl.!default {type hwcard 1}

from GeometryDash.soundplayer import SoundPlayer
import time

def soundTest():
# Sine tone during 0.1 s, blocking, device 0
    dev = 0 #maby auch 1 need test
    SoundPlayer.playTone(900, 0.1, True, dev) # 900 Hz
    SoundPlayer.playTone(800, 0.1, True, dev) # 600 Hz
    SoundPlayer.playTone(600, 0.1, True, dev) # 600 Hz
    time.sleep(1)
    SoundPlayer.playTone([900, 800, 600], 5, True, dev) # 3 tones together
    print ("done") 

def songStart(song):
    # Song, still to be done
    #song = SoundPlayer("C:/Users/ZOMFLAIG/Downloads/GeometryDash.mp3", 1) 
    song.play()

def songStop(song):
    song.stop()

