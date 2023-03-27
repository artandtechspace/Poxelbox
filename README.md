# Poxelbox

Was die Poxelbox ist und eine genaue Dokumentation des Systems findet man [hier](https://github.com/artandtechspace/Poxelbox-Dokumentation).


# Entwicklungsumgebung aufsetzen
Da die Software in Python3 entwickelt ist, wird empfohlen eine entsprechende IDE zu installieren.
Wir haben dafür [PyCharm](https://www.jetbrains.com/pycharm/) genommen, da es aktuelle und entsprechende Funktionen biete und Quelloffen ist, aber jede andere Entwicklungsumgebung geht selbstverständlich auch.

**Info: Unter Windows funktioniert der Webserver (Web-Config, Web-Config-Tool) nicht. Genauere Infos liegen in der 'Quirks & fuckups'-Sektion**

## Python-Packete
Aufgrund der Struktur der Hauptsoftware werden für die Entwicklungsumgebung andere Python-Packete verwendet als in der Produktionsumgebung.

Dies liegt daran, dass man auch ohne die Hardware der Poxelboxen oder externer Controller entwickeln können soll.

*In welcher Umgebung die Software startet kann über die `src/rsc/config.json` eingestellt werden. Mehr dazu in der untrigen Sektion 'Config'*

Daher werden in der **Entwicklungsumgebung** folgende Packete benötigt:

|Packet|Version|Befehl|Grund|
|-|-|-|-|
|[PyGame](https://pypi.org/project/pygame/)|`~=2.1.2`|```pip install pygame```|Simulieren der Poxelbox, Simulieren des Controllers|

und in der **Produktionsumgebung** folgende:

|Packet|Version|Befehl|Grund|
|-|-|-|-|
|[PySerial](https://pypi.org/project/pyserial/)|`~=3.5`|```pip install pyserial```|Eingaben des Controller-Adapter bzw. Controllers verarbeiten|
|Neopixel & GPIO/Board Librarys|Board: `~=1.0`||Ansprechen der Poxelboxen. Zum installieren am besten [dieser Anleitung](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage) folgen|

**außerdem** werden folgende Packete in **beiden** Umgebungen gebraucht
|Packet|Version|Befehl|Grund|
|-|-|-|-|
|[Flask](https://pypi.org/project/Flask/)|`~=2.2.2`|```pip install Flask```|Bereitstellung der Config-Schnittstelle und Hosting des Web-Config-Tools (mehr Infos unterhalb)|
|[Pillow](https://pypi.org/project/Pillow/)|`~=9.2.0`|```pip install Pillow```|Laden von Bildern und anderen Assets für die Spiele/Animationen|
|[NumPy](https://pypi.org/project/numpy/)|`~=1.23.3`|```pip install numpy```|Tetris... ja wirklich|
|[varname](https://pypi.org/project/varname/)|```pip install varname```|Generische Vektoren|

Um die Installationen zu vereinfachen werden hier außerdem die jeweiligen [requirements.txt](https://learnpython.com/blog/python-requirements-file/)-Dateien angegeben

---

**Entwicklungsumgebung:**
```
Pillow~=9.2.0
pygame~=2.1.2
varname~=0.10.0
numpy~=1.23.3
Flask~=2.2.2
```

---

**Produktionsumgebung:**
```
pygame~=2.1.2
board~=1.0
pyserial~=3.5
numpy~=1.23.3
varname~=0.10.0
Flask~=2.2.2
```

---

## Setup
**Bei Problemen im Setup bitte zuerst einmal in der Sektion 'Quirks & fuckups' schauen**

Die Datei `src/__init__.py` ist die Haupt-Startdatei und muss so auch ausgeführt werden:

```
python __init__.py
```

### Produktionsumgebung

Es wird empfehlen in der Produktionsumgebung einen Linux-[Service](https://linuxhandbook.com/create-systemd-services/) zu erstellen, welcher das Program nach beenden neustartet und auch beim Raspberry-Pi-start startet.

---

Erstelle und Bearbeite mittels

```bash
nano /etc/systemd/system/Poxelbox.service
```

die Poxelbox-Service-Datei.

Hier wird folgende Konfiguration eingefügt:
```ini
[Unit]
Description=Service-Worker for the poxelbox
StartLimitIntervalSec=0


[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/usr/bin/python3.9 /home/ledwand/Poxelbox/src/__init__.py
WorkingDirectory=/home/ledwand/Poxelbox/src/

[Install]
WantedBy=multi-user.target
```

Hier wird davon ausgegangen, dass der Pi-Benutzer `ledwand` heißt, die Python-Executeable in `/usr/bin/python3.9` liegt und das Program unter `/home/ledwand/Poxelbox/` zu finden ist.

Sollte das bei dir anders sein, passe bitte folgende Zeilen in deiner Konfiguration an:

```ini
ExecStart=/usr/bin/python3.9 /home/ledwand/Poxelbox/src/__init__.py
WorkingDirectory=/home/ledwand/Poxelbox/src/
```

Wobei `ExecStart` der Befehl ist, welcher ausgeführt wird, sobald der Service startet und `WorkingDirectory` das Verzeichnis angibt in welchem der Befehl ausgeführt wird.


Nach erstellen der Servicedatei, können wir diese starten

```bash
service Poxelbox start
```

und automatisch für den autostart bei einem Raspberry-Pi-neustart konfigurieren:

```bash
service Poxelbox enable
```

# Config
Die `src/rsc/Config.json` ist im endeffekt nur der Speicherort der Konfiguration und exakt gleich den Möglichkeiten, welche die Konfigurations-tools bieten.

Für eine genaue Erklärung, wie die Konfiguration funktioniert, bitte einen Blick in die 'Konfiguration der Haupt-Software'-Sektion des [Dokumentations-Repositorys](https://github.com/artandtechspace/Poxelbox-Dokumentation) werfen.


# Hosting des Web-Config-Tools

Auch wenn das [Web-Config-Tool](https://github.com/artandtechspace/Poxelbox-Configtool-Web) selber unabhängig von der Haupt-Software ist, wird trotzdem immer ein Build von diesem mit der Hauptsoftware ausgeliefert um schnellen Zugriff auf die Konfiguration von außerhalb zu erhalten.

Dieser Build liegt unter `rsc/webserver/Poxelbox-Configtool-Web/`, wobei `Poxelbox-Configtool-Web` als Git-[Sub-Module](https://www.atlassian.com/git/tutorials/git-submodule) eingebunden ist.

Hierfür enthält das `Poxelbox-Configtool-Web`-Repo einen extra Branch, welcher außschließlich einen Ordner `app` mit dem Build der Webapp enthält.

Um diesen Ordner zu initialisieren, bitte folgenden Befehl im Root-Ordner des Poxelbox-Hauptsoftware-Projektes, als `src/` ausführen:

```bash
git submodule init
git submodule update
```

# Quirks & fuckups

## Windows
Aufgrund von systematischen Unterschieden bei der Erstellung von Unterprozessen zwischen Window und Linux bzw. Unix, müssen wir den Webserver (Flask) unter Windows deaktivieren, weshalb hier nur eine Entwicklung der Hauptsoftware möglich ist.

Das genaue Problem wird in [diesem Artikel](https://www.pythonforthelab.com/blog/differences-between-multiprocessing-windows-and-linux/) genauer beschrieben.
