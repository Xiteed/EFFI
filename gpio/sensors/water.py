import time
from grove.adc import ADC
from db_handling import upload_data

MOIS = 0


def measure_moisture():  # Grove - Moisture Sensor connected to port D2
    global MOIS
    sensor = GroveMoistureSensor(2)
    while True:
        mois = sensor.read()
        if mois != MOIS:
            MOIS = humi
            payload = f"mois_test moisture={mois}\n"
            upload_data(payload)
        time.sleep(1)


if __name__ == '__main__':
    try:
        measure_moisture()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt, cleanup is done")
