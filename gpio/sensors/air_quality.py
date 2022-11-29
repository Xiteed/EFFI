import time
from seeed_dht import DHT
from db_handling import upload_data

HUMI = 0
TEMP = 0


def measure_temp_hum():  # Grove - Temperature&Humidity Sensor connected to port D5
    global HUMI, TEMP
    sensor = DHT('11', 5)
    while True:
        humi, temp = sensor.read()
        if humi != HUMI or temp != TEMP:
            HUMI = humi
            TEMP = temp
            payload = f"temp_test temperature={temp},humidity={humi}\n"
            upload_data(payload)
        time.sleep(1)


if __name__ == '__main__':
    try:
        measure_temp_hum()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt, cleanup is done")
