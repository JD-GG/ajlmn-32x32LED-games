import threading
import os

class SoundPlayer:
    '''
    Sound player based on SoX, called "the Swiss Army knife of sound processing programs" by its developer.
    This simple Python wrapper is based on Linux shell commands running in extra threads. 
    For the Raspberry Pi the following installations are needed:
    sudo apt-get install sox
    sudo apt-get install mp3
    '''

    @staticmethod
    def playTone(frequencies, duration, blocking=False, device=0):
        '''
        Plays one or several sine tones with given frequencies and duration.
        @param frequencies: the frequency or a list of several frequencies in Hz
        @param duration: the duration in s
        @param blocking: if True, the functions blocks until playing is finished; otherwise it returns immediately (default: False)
        @param device: the sound device ID (e.g. 0: standard device, 1: USB sound adapter)
        '''
        if not isinstance(frequencies, list):
            frequencies = [frequencies]
        if blocking:
            SoundPlayer._emit(frequencies, duration, device)
        else:
            threading.Thread(target=SoundPlayer._emit, args=(frequencies, duration, device)).start()

    @staticmethod
    def isPlaying():
        '''
        Checks if the sound is still playing.
        @return: True, if the sound is playing; otherwise False
        '''
        info = os.popen("ps -Af").read()
        process_count = info.count("play")
        return process_count >= 2

    @staticmethod
    def _emit(frequencies, duration, device):
        s = " "
        for f in frequencies:
            s += "sin " + str(f) + " "
        cmd = "AUDIODEV=hw:" + str(device) + " play -q -n synth " + str(duration) + \
            s + " 2> /dev/null" 
        os.system(cmd)

    def __init__(self, audiofile, device=0):
        '''
        Creates a sound player to play the given audio file (wav, mp3, etc.) 
        to be played at given device ID. Throws exception, if the sound resource is not found.
        @param audiofile: the sound file to play
        @param device: the sound device ID (e.g. 0: standard device, 1: USB sound adapter)
        '''
        if not os.path.isfile(audiofile):
            raise Exception("Audio resource " + audiofile + " not found")
        self.audiofile = audiofile
        self.device = device
 
    def _run(self, cmd):
        os.system(cmd)

    def play(self, volume=1, blocking=False):
        '''
        Plays the sound with given volume (default: 1). The function returns immediately.
        @param volume: the sound level (default: 1)
        @param blocking: if True, the functions blocks until playing is finished; otherwise it returns immediately (default: False)
        '''
        self.volume = volume
        cmd = "AUDIODEV=hw:" + str(self.device) + \
            " play -v " + str(self.volume) + \
            " -q " + self.audiofile + " 2> /dev/null"

        if blocking:
            self._run(cmd)
        else:
            threading.Thread(target=self._run, args=(cmd,)).start()

    @staticmethod
    def stop():
        '''
        Stops playing.
        '''
        cmd = "sudo killall -9 play"
        threading.Thread(target=SoundPlayer._run, args=(cmd,)).start()

    @staticmethod
    def pause():
        '''
        Pauses playing momentarily.
        '''
        cmd = "sudo pkill -STOP play"
        threading.Thread(target=SoundPlayer._run, args=(cmd,)).start()

    @staticmethod
    def resume():
        '''
        Resumes playing (after it has been stopped).
        '''
        cmd = "sudo pkill -CONT play"
        threading.Thread(target=SoundPlayer._run, args=(cmd,)).start()
