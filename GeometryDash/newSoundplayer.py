import subprocess

class AudioPlayer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.process = None

    def play(self):
        # Start playing the audio file
        self.process = subprocess.Popen(["aplay", self.file_path])

    def stop(self):
        # Terminate the process if it's running
        if self.process:
            self.process.terminate()
