# Gruppen Repository von ajlmn für 32x32 Matrix Spielekonsole (Gruppe 3)
Wir als Gruppe ajlmn haben uns entschieden auf der 32x32 Matrix die Spiele FlappyBird,
GeometrieDash sowie Snake zu programmieren. Diese sind in den unter Ordnern mit entsprechenden
Namen zu finden. Gespielt wird auf einem Raspberry PI 3 mit einem Joypad. Für Geometry Dash wird ein externes Soundsystem empfohlen.

Repo: https://github.com/JD-GG/ajlmn-32x32LED-games

## Projektaufbau
Die Datei Startscreen.py wird von dem Atostart-Service aufgerufen. Startscreen.py kann natürlich auch manuell gestartet werden.  

Hier wird eine globale Matrix und ein globaler Screen definiert. Jedes Spiel in seinem eigenem Unterordner ist ein Python-Modul. Jedes Spiel hat eine Hauptfunktion die von Startscreen.py aus aufgerufen wird. Alle Spiele und der Auswahlbildschirm teilen sich einen Screen und eine Matrix um Komplikationen zu verhindern. 

Wenn ein Spiel zu ende ist startet es neu. Mit der SELECT-Taste kann zum Auswahl-Bildschrim zurückgekehrt werden. 

Vom Auswahl-Bildschrim aus kann auch das Programm und der PI beendet / herunter gefahren werden.

Zum steuern werden immer alle Knöpfe (außer SELECT) als input gewertet. Oder das 4-Axis Kreuz. 

Das gesammte Programm verhält sich unterschiedlich wenn es auf dem PI oder auf einem PC gestartet geworden ist. Dies erleichterte den development Prozess und benötigt keine unnötigen Resourcen auf dem PI/PC.

## StartScreen.py
Logik für die Erkennung des Gerätes
```Python
started_on_pi = True
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    print("Library rgbmatrix imported successfully!")
except ImportError:
    started_on_pi = False
    print("Library rgbmatrix import failed!")
```
Gemeinsam genutze Matrix und canvas
```Python
# Configuration for the matrix
matrix = None
offset_canvas = None
if started_on_pi:
    options = RGBMatrixOptions()
    options.rows = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'
    options.drop_privileges = 0# DONT DROP PRIVS!!!

    # Matrix & Canvas
    matrix = RGBMatrix(options = options)
    offset_canvas = matrix.CreateFrameCanvas()
```

und Screen. Der Screen ist breiter auf dem PC und zeigt links den Pygame-Bildschirm + Debug optionen. Rechts ist die Matrixrepresäntation.

```Python
# Setup screen for ALL GAMES
screen = None
if started_on_pi:
    screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
else:
    screen = pygame.display.set_mode((s.SCREEN_WIDTH*2, s.SCREEN_HEIGHT))
pygame.display.set_caption("Startscreen")
```
Auswahl der Spiele. Übergabe für die Spiel-Funktionen sind die globalen Screen, Matrix und Canvas Variablen.
```Python
# Start selected Game
        elif event.type == pygame.JOYBUTTONDOWN and event.button != 8:
            if(select_box_x == 0 and select_box_y == 0):
                flappy_bird_game(screen, matrix, offset_canvas)
            elif(select_box_x == 0 and select_box_y == SCREEN_HALF):
                snake_game(screen, matrix, offset_canvas)
            elif(select_box_x == SCREEN_HALF and select_box_y == 0):
                geometry_dash_game(screen, matrix, offset_canvas)
            elif(select_box_x == SCREEN_HALF and select_box_y == SCREEN_HALF):
                run = False
```

## FlappyBird (Modul)
### FlappyBird.py
Aufbau:  
- Initialisiere Variablen
- Haupt Gameloop
  - Player Physiks
  - Pillar Physics
  - Edgecases
  - Pillar kolision
  - Score increment
  - Event listeners
  - Drawing  
  - draw_matrix

Die Funktionen sind in unterschiedliche Dateien verteilt. Die haupt Spielfunktion befindet sich in FlappBird.py
```Python
def flappy_bird_game(screen, matrix, offset_canvas):
```
### colors.py
Hier werden Farben definiert
### mapGeneration.py
Bestimmung der zufälligen Positionen von den Pillars.
### output.py
Hier befinden sich allgemein genutzte Funktionen. Diese Funktion wird in jedem Modul genutzt um die Matrix an zu steuern.
```Python
def draw_matrix(screen, matrix, offset_canvas):
    for y in range(32):
        for x in range(32):
            pos_x = x * s.PIXEL_WIDTH
            pos_y = y * s.PIXEL_WIDTH
            color = screen.get_at((pos_x, pos_y + s.DOWNWARD_PIXEL_PULL_OFFSET))# get color in format (r, g, b, t)            
            offset_canvas.SetPixel(x, y, color[0], color[1], color[2])
    return matrix.SwapOnVSync(offset_canvas)
```
Aber auch FlappyBird spezifische Funktionen.
```Python
def draw_hitboxes(screen, player_hitbox, pillar_pos_x, pillar_hitbox_top, pillar_hitbox_score, pillar_hitbox_bottom):
    pygame.draw.rect(screen, (255, 0, 0), player_hitbox, 3)  # width = 3
    for i in range(s.PILLAR_COUNT):
        if pillar_pos_x[i] < s.SCREEN_WIDTH:
            pygame.draw.rect(screen, (255, 0, 0), pillar_hitbox_top[i], 3)  # width = 3
            pygame.draw.rect(screen, (255, 0, 0), pillar_hitbox_score[i], 3)  # width = 3
            pygame.draw.rect(screen, (255, 0, 0), pillar_hitbox_bottom[i], 3)  # width = 3
```
### score.py
Zahlen von 1-9 in 2-Dimensionaler Darstellung
### settings.py
Konstanten für FlappyBird

## GeometryDash (Modul)
### Main.py
Aufbau:
- Initialisiere Variablen
- Außere Gameloop
  - Musik start & stop
  - Innere Gameloop
    - Kollision
	- Drawing & Gamelogik
	- User Input
	- Draw Score
	- draw_matrix
### collision.py
Hier werden Kollisionen mit dem Boden, Todesobjekten und Blöcken verarbeitet.
### drawing.py 
Hier werden Spieler, Blöcke und die Prozentanzeige gezeichnet. Es befindet sich auch die von der Rechenleistung her aufwendigste Funktion in dieser Datei.
```Python
def drawObstical(screen)
```
### newSoundplayer.py
Initialisiert, Startet und Stopt die Musik sowie die anderen Sounds. Nutzt den Konsolen-Befehl aplay und startet einen neuen Subprozess.
```Python
self.process = subprocess.Popen(["aplay", self.file_path])
```
### test.py
Nur kleine test Funktionen, nichts relevantes für das Spiel.
### userInput.py
Regelt den userInput für Tastatur sowie controller. S/Select um in den Homescreen zu kommen, Space/ControllerTasten um zu Springen.
### Variables.py
Beherbergt Konstanten sowie globale Variabeln wie z.b. Die Map Parts und die Scorekonstanten

## Snake (Modul)
### Snake.py
Aufbau:  
- Initialisiere Variablen
- Snake Class
- Apple Class
- Haupt Gameloop
  - Click Events
  - Aufrufen von Update Methoden von Snake und Apple für collisions
  - Drawing
  - remove apple when eaten
  - draw_matrix

Diese Funktion checkt ob die Snake tot ist innerhalb von der Snake Class
```Python
if self.dead:
                self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
                self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
                self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
                self.xdir = 1
                self.ydir = 0
                self.dead = False
                apple = Apple()
```

## Aufgabenverteilung
### FlappyBird
- Luca
- Noah
- Jan-David

### Geometrie Dash 
- Aaron
- Moritz

### Snake
- Noah

### Hardware & Sonstiges
- Moritz
- Aaron
- Jan-David  

Siehe auch unser Trello-Board für Details:  
https://trello.com/b/wJnBBpKd/gruppe-3

## Deployment
### Hardware
Raspberry PI 3  
32x32 LED Matrix mit Hat  
Externe USB-Audio Karte  
Lautsprecher verbunden mit externer Soundkarte  
Joypad

### Instaliere Betreibssystem
Raspberry Pi OS (64 Bit)

### Standard update Befehle
sudo apt update  
sudo apt upgrade

### Installiere python3
sudo apt install python3 python3-pip

### Installiere Matrix Bibliothek und führe Install-Script aus
cd ~  
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/
rgb-matrix.sh >rgb-matrix.sh  
sudo bash rgb-matrix.sh  
```
	> Continue Y
	> Select 2 Hat + RTC
	> Select 1 Quality (Requires soldering)
```

### Clone git repo in das Home-Verzeichnis
cd ~  
git clone https://github.com/JD-GG/ajlmn-32x32LED-games.git  

### Erstelle Autostart Servicefile und aktiviere Service
sudo nano /etc/systemd/system/MatrixGames.service
```
	[Unit]
	Description=MatrixGames
	After=multi-user.target
	
	[Service]
	Type=simple
	ExecStart=/usr/bin/python3 /home/pi/ajlmn-32x32LED-games/StartScreen.py
	WorkingDirectory=/home/ajlmn-32x32LED-games/
	Restart=on-failure
	
	[Install]
	WantedBy=multi-user.target
```
sudo systemctl daemon-reload  
sudo systemctl enable MatrixGames.service

### Ändere default audio device auf externe Karte
sudo nano /usr/share/alsa/alsa.conf  
```
	<<<
	defaults.ctl.card 0
	defaults.pcm.card 0
	>>>
	defaults.ctl.card 1
	defaults.pcm.card 1
```

### Deaktiviere built in Audio
sudo nano /etc/modprobe.d/raspi-blacklist.conf
```
	blacklist snd_bcm2835
```

### Reboot and enjoy
sudo reboot