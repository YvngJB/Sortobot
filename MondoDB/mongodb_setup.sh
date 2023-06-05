#!/bin/bash

# MongoDB Installation
# sudo apt update
# sudo apt install mongodb -y

# MongoDB-Server-Konfiguration
sudo sed -i 's/#sharding:/sharding:\n  clusterRole: "configsvr"/' /etc/mongodb.conf
sudo sed -i 's/#replication:/replication:\n  replSetName: "configReplSet"/' /etc/mongodb.conf
sudo sed -i 's/bindIp: 127.0.0.1/bindIp: 0.0.0.0/' /etc/mongodb.conf

# Firewall-Konfiguration mit UFW oder iptables
if command -v ufw &> /dev/null; then
    sudo ufw status
    sudo ufw allow 27017
    sudo ufw enable
else
    sudo iptables -A INPUT -p tcp --dport 27017 -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT
    sudo iptables-save | sudo tee /etc/iptables/rules.v4
fi

# MongoDB-Server starten
sudo service mongodb start

# Initialisierung des Sharding-Clusters
mongo <<EOF
use admin
sh.enableSharding("test")
db.test.createIndex({ "color": 1 })
sh.shardCollection("test.data", { "color": 1 })
EOF

# Hinzufügen von Shards
mongo <<EOF
use config
sh.addShard("rot/localhost:27017")
sh.addShard("gruen/localhost:27017")
sh.addShard("blau/localhost:27017")
EOF

# Überprüfung der Sharding-Konfiguration
mongo <<EOF
use config
sh.status()
EOF

# Daten schreiben
mongo <<EOF
use test
db.data.insert({ "color": "rot", "name": "Objekt 1" })
EOF

# Überprüfung der Verteilung
mongo <<EOF
use test
sh.status()
EOF
