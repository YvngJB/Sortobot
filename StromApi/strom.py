import requests
from datetime import datetime, timedelta
import json

now = datetime.now()
start_date = int(now.timestamp() * 1000)
end_date = int((now + timedelta(days=2)).timestamp() * 1000)

url = f"https://api.awattar.de/v1/marketdata?start={start_date}&end={end_date}"
response = requests.get(url)

status_code = response.status_code

if status_code == 200:
    try:
        data = response.json()
        min_price = float("inf")
        min_price_time = None

        for price in data['data']:
            timestamp = price['start_timestamp']
            value = price['marketprice']

            if value < min_price:
                min_price = value
                min_price_time = timestamp

        if min_price_time is not None:
            datetime_obj = datetime.fromtimestamp(min_price_time / 1000)
            formatted_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Guenstigster Strompreis: {min_price} Euro/kWh um {formatted_time}")
        else:
            print("Keine Daten gefunden.")
    except json.JSONDecodeError as e:
        print("Fehler beim Decodieren der API-Antwort:", e)
else:
    print("Fehler beim Abrufen der Strompreise. Statuscode:", status_code)
