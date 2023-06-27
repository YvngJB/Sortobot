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
