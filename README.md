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


Verlauf: 
  - Nach Aufgabenstellung mussten wir auf einer VM eine MongoDB Datenbank installieren, der die Methode des Shardings zugrunde liegt
  - Auf dieser haben wir dann die Messdaten gelogt, die vom PC1 übermittelt wurden
  - Um eine Benutzerfreundliche Ansicht der Daten zu gewährleisten, haben wir diese per NodeRed visualisiert. So können nun jegliche Endgeräte auf diese Informationen zureifen  
