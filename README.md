# Gruppen Repository von ajlmn für 32x32 Matrix Spielekonsole (Gruppe 3)
Wir als Gruppe ajlmn haben uns entschieden auf der 32x32 Matrix die Spiele FlappyBird,
GeometrieDash sowie Snake zu programmieren. Diese sind in den unter Ordnern mit entsprechenden
Namen zu finden. Gespielt wird auf einem Raspberry PI 3 mit einem Joypad. Für Geometry Dash wird ein externes Soundsystem empfohlen.

## Projektaufbau
Die Datei Startscreen.py wird von dem Atostart-Service aufgerufen. Startscreen.py kann natürlich auch manuell gestartet werden.  

Hier wird eine globale Matrix und ein globaler Screen definiert. Jedes Spiel in seinem eigenem Unterordner ist ein Python-Modul. Jedes Spiel hat eine Hauptfunktion die von Startscreen.py aus aufgerufen wird. Alle Spiele und der Auswahlbildschirm teilen sich einen Screen und eine Matrix um Komplikationen zu verhindern. 

Wenn ein Spiel zu ende ist startet es neu. Mit der SELECT-Taste kann zum Auswahl-Bildschrim zurückgekehrt werden. 

Vom Auswahl-Bildschrim aus kann auch das Programm und der PI beendet / herunter gefahren werden.

Zum steuern werden immer alle Knöpfe (außer SELECT) als input gewertet. Oder das 4-Axis Kreuz. 

Das gesammte Programm verhält sich unterschiedlich wenn es auf dem PI oder auf einem PC gestartet geworden ist. Dies erleichterte den development Prozess und benötigt keine unnötigen Resourcen auf dem PI/PC.

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