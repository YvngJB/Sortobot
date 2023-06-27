# scan.py - class that holds information about one scan
from datetime import datetime

class Scan:
    def __init__(self, _id: int, timestamp: str, color: str, temperature: float, humidity: float, duration: float, costs: float) -> None:
        self._id = _id
        self.timestamp = timestamp
        self.color = color
        self.temperature = temperature
        self.humidity = humidity
        self.duration = duration
        self.costs = costs
    
    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "timestamp": self.timestamp,
            "color": self.color,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "duration": self.duration,
            "costs": self.costs
        }

    def __str__(self) -> str:
        return f"Scan({self.timestamp}, {self.color}, {self.temperature}, {self.color})"