from datetime import datetime

#scan sammelt alle daten während eines scans
class Scan:
    def __init__(self,_id: int, timestamp: str, color: str, temperature: float, humidity: float, duration: float, costs: float) -> None :
        self._id = _id
        self.timestamp = timestamp
        self.color = color
        self.temperature = temperature
        self.humidity = humidity
        self.duration = duration
        self.costs = costs

# write_dict um abgerufene Attribute in ein Wörterbuch umzuwandeln
    def write_dict(self) -> dict:
        return {
            "_id": self._id,
            "timestamp": self.timestamp,
            "color": self.color,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "duration": self.duration,
            "costs": self.costs,
        }


 # __repr__ um eine repräsentative Zeichenfolge zurückzugeben, die den vollständigen Zustand des Objekts darstellt.
    def __repr__(self) -> str:
        return f"Scan({self._id}, {self.timestamp}, {self.color}, {self.temperature}, {self.humidity}, {self.duration}, {self.costs})"



#Scan()