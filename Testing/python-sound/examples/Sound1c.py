# Sound1c.py

from soundplayer import SoundPlayer
import RPi.GPIO as GPIO
import time

'''
states:
STOPPED : play process terminated
PAUSED: play process stopped (playing still underway)
PLAYING: play process executing
'''

# Button pins, adapt to your configuration
P_PLAY = 24 
P_PAUSE = 16
P_STOP = 22
P_SELECT = 12

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(P_STOP, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(P_PAUSE, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(P_PLAY, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(P_SELECT, GPIO.IN, GPIO.PUD_UP)
 
setup()
nbSongs = 4
songID = 0
state = "STOPPED"
print "ready->stopped"
p = SoundPlayer("/home/pi/songs/song" + str(songID) + ".mp3", 1)        

while True:
    if GPIO.input(P_PAUSE) == GPIO.LOW and state == "PLAYING":
        state = "PAUSED"
        p.pause()
        print "playing->paused"
    elif GPIO.input(P_PLAY) == GPIO.LOW and state == "STOPPED":
        state = "PLAYING"
        p.play()
        print "stopped->playing, song ID", songID
    elif GPIO.input(P_PLAY) == GPIO.LOW and state == "PAUSED":
        state = "PLAYING"
        p.resume()
        print "paused->playing"
    elif GPIO.input(P_STOP) == GPIO.LOW and (state == "PAUSED" or state == "PLAYING"):
        state = "STOPPED"
        p.stop()
        print "paused/playing->stopped"
    elif GPIO.input(P_SELECT) == GPIO.LOW and state == "STOPPED":
        songID += 1
        if songID == nbSongs:
            songID = 0
        p = SoundPlayer("/home/pi/songs/song" + str(songID) + ".mp3", 1)
        print "stopped->playing, song ID", songID
        p.play()
        state = "PLAYING"
    if state == "PLAYING" and not p.isPlaying():
        print "finished->stopped"
        state = "STOPPED"      
    time.sleep(0.1)    
