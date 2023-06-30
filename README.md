# Sortobot
DoBot Projekt Adam, Jannis, Dominik, Jason

# Inhaltsverzeichnis 
  1) Raspberry Pi
  2) PC1
  3) PC2

# 1) Raspberry Pi
Aufgaben des Raspberry Pi's:
  - Auslesen der Farbe des Würfels
  - Auslesen der Temperatur
  - Übermitteln der Daten an PC1

Verlauf:
  - Im ersten Schritt haben wir dem Raspberry Pi eine feste IP zugewiesen und einen Zugriff per SSH aktiviert
  - Erste Versuche auf den Raspberry Pi per SSH zuzugreifen, waren erfolgreich
  - Im nächsten Schritt haben wir den Temperatursensor, sowie die Kamera am Raspberry Pi angeschlossen
  - Zum auslesen der Temperaturdaten hatten wir aus dem vorherigen Halbjahr ein Python Script, welches wir Recyceln konnten
  - Für die Kamera mussten wir einen Code entwickeln, der die Farbe ausliest
  - Das Übermitteln der Daten auf PC1 erfolgt dann mittels TCP/IP 


# Dokumentation: Farberkennung mit OpenCV und Raspberry Pi

Der  Code ist eine Implementierung zur Farberkennung mithilfe der OpenCV-Bibliothek auf einem Raspberry Pi. Er ermöglicht das Erfassen eines Bildes von der Kamera, die Extraktion eines zentralen Ausschnitts und die Bestimmung der vorherrschenden Farbe in diesem Ausschnitt.

Um den Code auszuführen, müssen zunächst die erforderlichen Abhängigkeiten installiert werden. Dies kann mit den folgenden Befehlen auf einem Raspberry Pi erfolgen:

```
sudo apt update
sudo apt install python3-opencv
sudo apt install python3-numpy
```

Nach der Installation der Abhängigkeiten kann der folgende Code verwendet werden:

```python
import sys
import cv2
import numpy as np
from PIL import Image
import keyboard
import time
import datetime
from scan import Scan
```

Der Code beginnt mit den erforderlichen Importanweisungen, um die verwendeten Bibliotheken und Module zu importieren. Diese umfassen `sys`, `cv2` aus OpenCV für die Kamerasteuerung und Bildverarbeitung, `numpy` für numerische Berechnungen, `Image` aus PIL für die Bildmanipulation, `keyboard` für die Tastatureingabe, `time` für die Zeitsteuerung und `datetime` für die Zeitangabe. Zusätzlich wird `scan` importiert, was vermutlich eine benutzerdefinierte Klasse ist, die nicht im gegebenen Codeausschnitt enthalten ist.

```python
class Camera:
    def __init__(self, camera_index=0) -> None:
        self._camera = cv2.VideoCapture(camera_index)
        self._last_capture_time = 0
```

Die Klasse `Camera` dient als Schnittstelle zur Kamera des Raspberry Pi. In der `__init__`-Methode wird die Kamera initialisiert und ein Zeitzähler `_last_capture_time` auf 0 gesetzt.

```python
    def _capture(self, absolute_path: str) -> None:
        current_time = time.time()
        if current_time - self._last_capture_time >= 3:
            ret, frame = self._camera.read()
            if ret:
                height, width, _ = frame.shape
                center_x, center_y = width // 2, height // 2
                crop_size = 250
                crop = frame[center_y - crop_size // 2: center_y + crop_size // 2,
                             center_x - crop_size // 2: center_x + crop_size // 2]
                cv2.imwrite(absolute_path, crop)
                self._last_capture_time = current_time
```

Die Methode `_capture` erfasst ein Bild von der Kamera und speichert es in einem angegebenen Dateipfad. Die Aufnahme erfolgt nur, wenn seit der letzten Aufnahme mindestens 3 Sekunden vergangen sind. Das aufgenommene Bild wird zugeschnitten, indem ein zentraler Ausschnitt mit einer Größe von 250x250 Pixeln ausgewählt wird. Dieser Ausschnitt wird dann als JPEG-Bild im angegebenen Pfad gespeichert.

```python
    def _get_rgb(self) -> tuple:
        try:
            self._capture("temp.jpg")
            img = cv2.imread("temp.jpg")
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            lower_red = np.array([0,

 50, 50])
            upper_red = np.array([10, 255, 255])
            lower_green = np.array([50, 50, 50])
            upper_green = np.array([70, 255, 255])
            lower_blue = np.array([100, 50, 50])
            upper_blue = np.array([130, 255, 255])
            lower_yellow = np.array([20, 50, 50])
            upper_yellow = np.array([40, 255, 255])

            mask_red = cv2.inRange(img_hsv, lower_red, upper_red)
            mask_green = cv2.inRange(img_hsv, lower_green, upper_green)
            mask_blue = cv2.inRange(img_hsv, lower_blue, upper_blue)
            mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

            contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            contours = [contours_red, contours_green, contours_blue, contours_yellow]
            max_contour_area = 0
            max_contour_color = None
            for i, color_contours in enumerate(contours):
                if len(color_contours) > 0:
                    contour_area = max(cv2.contourArea(contour) for contour in color_contours)
                    if contour_area > max_contour_area:
                        max_contour_area = contour_area
                        max_contour_color = i

            colors = ["Red", "Green", "Blue", "Yellow"]
            if max_contour_color is not None:
                print("[+] Detected color is : " , colors[max_contour_color])
                return colors[max_contour_color]
            else:
                return None

        except (FileNotFoundError, cv2.error) as e:
            print(f"Error: {e}")
            return None
```

Die Methode `_get_rgb` verwendet das zuvor definierte `_capture`, um ein Bild aufzunehmen und die Farben darin zu erkennen. Zuerst wird das aufgenommene Bild geladen und in den HSV-Farbraum konvertiert. Anschließend werden Farbschwellenwerte für Rot, Grün, Blau und Gelb definiert, um Farbbereiche zu bestimmen.

Mit diesen Schwellenwerten werden Masken erstellt, die die Bereiche im Bild markieren, die den Farben entsprechen. Die Masken werden dann verwendet, um Konturen zu finden, die die erkannten Farbbereiche darstellen. Für jede Farbe wird die Kontur mit der größten Fläche ausgewählt.

Die erkannte Farbe wird als Text ausgegeben, und der Name der Farbe wird als Rückgabewert der Methode verwendet. Falls keine Farbe erkannt wird oder ein Fehler auftritt, wird `None` zurückgegeben.

```python
    def scan(self):
        rgb = self._get_rgb()
        if rgb is not None:
            return rgb
        else:
            return None
```

Die Methode `scan` ruft `_get_rgb` auf und gibt den erkannten Farbwert zurück, sofern einer erkannt wurde. Andernfalls wird `None` zurückgegeben.

#
# 2) PC1
Aufgaben des PC1:
  - Steuerung des Roboters
  - Übermitteln der Daten an PC2

Verlauf:
  - Wir mussten einen Code entwickeln, die dem Roboter sagt, wo ein Würfel hochzuheben ist, wo er danach zum auslesen der Farbe hinfahren soll und wo letzten Endes der Würfel, basierend auf seiner Farbe, abgelegt werden soll
  - Diese Daten werden dann, samt der Daten des Raspberry Pi's, per TCP/IP an PC2 übertragen

# 3) PC2
Aufgaben des PC2:
  - Installation eines DB Servers
  - Installation eines MQTT Servers
  - Bereitstellen der Daten per NodeRed

Verlauf: <br>
Nach Aufgabenstellung mussten wir auf einer VM eine MongoDB Datenbank installieren, der die Methode des Shardings zugrunde liegt:

Schritt 1: Erstellen der Verzeichnisse

 > mkdir mongo
 > mkdir con1 con2 shard10 shard11 shard20 shard21

Schritt 2: Konfigurationsserver einrichten

 > mongod --configsvr --dbpath con2 --port 20002 --fork --logpath con2.log -- replSet con

Schritt 3: Replica Set für den Konfigurationsserver initialisieren

Shell starten:

 > mongo --port 20001

In der Shell das Replica Set für den Konfigurationsserver initialisieren:

  > rs.initiate()
  > rs.add("localhost:20002")
  > rs.status()
  > exit

Schritt 4: Shardserver für Shard 1 einrichten

Shard1 - Server1:
 > mongod --shardsvr --replSet shard1 --dbpath shard10 --port 21001 --fork --logpath shard1.log

Shard1 - Server2:
 > mongod --shardsvr --replSet shard1 --dbpath shard11 --port 21002 --fork --logpath shard1.log

Schritt 5: Replica Set für Shard 1 initialisieren

Shell starten:

 > mongo --port 21001

In der Shell das Replica Set für den Shard 1 initialisieren:

  > rs.initiate()
  > rs.add("localhost:21002")
  > exit

Schritt 6: Shardserver für Shard 2 einrichten

Shard 2 - Server 1:

 > mongod --shardsvr --replSet shard2 --dbpath shard20 --port 22001 --fork --logpath shard2.log

Shard 2 - Server 2:

 > mongod --shardsvr --replSet shard2 --dbpath shard21 --port 22002 --fork --logpath shard2.log

Schritt 7: Replica Set für Shard 2 initialisieren:

Shell starten:

  >mongo --port 22001

In der Shell das Replica Set für den Shard 2 initialisieren:

  > rs.initiate()
  > rs.add("localhost:22002")
  > exit

Schritt 8: Mongos-Prozess starten

 > mongos --configdb "con/localhost:20001,localhost:20002" --fork --logpath mongos1.log --port 20000

Schritt 9: Verbinden mit dem Mongos-Prozess und Konfigurieren der Shards

MongoDB Shell öffnen:

 > mongo --port 20000

Shards konfigurieren:

  > sh.addShard("shard1/localhost:21001")
  > sh.addShard("shard2/localhost:22001")

Schritt 10: Sharding aktivieren

Datenbank anlegen:

 > use team7

Sharding für die Datenbank aktivieren:

 > sh.enableSharding("team7")

Eine Sammlung erstellen die geshardet werden soll:

>  db.createCollection("scans")

Sharden der erstellten Sammlung:

 > sh.shardCollection("team7.scans", {_id:1})

  
        
  - Auf dieser haben wir dann die Messdaten gelogt, die vom PC1 übermittelt wurden
  - Um eine Benutzerfreundliche Ansicht der Daten zu gewährleisten, haben wir diese per NodeRed visualisiert. So können nun jegliche Endgeräte auf diese Informationen zureifen  
