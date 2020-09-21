import Adafruit_DHT
import postgresql
import json
import time

db = postgresql.open('pq://alex:2123qQ@localhost/casa')
channelsId={
    "2":2,
    "3":3,
    "1":4,
    "0":5
}


DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 3

print("Inicio sensor de temperatura local")

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        
        prepareTemp= db.prepare("INSERT INTO  temperaturas_rf_temperature (temp, humidity, sensor_id, date) VALUES ($1, $2, $3, NOW())")
        prepareTemp(
            temperature,
            humidity,
            channelsId[str(0)]
            )
        prepareSensor= db.prepare("UPDATE temperaturas_rf_sensor SET  last_updated=NOW() where channel=$1")
        prepareSensor("0")
        time.sleep(60*5)
    else:
        print("no encontrado")
