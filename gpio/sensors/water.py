import time
import math
from grove.adc import ADC
from db_handling import upload_data
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.grove_moisture_sensor import GroveMoistureSensor


MOIS = 0
DIST = 0


def main():
    global MOIS, DIST
    moisture_sensor = GroveMoistureSensor(2)
    distance_sensor = GroveUltrasonicRanger(16)
    while True:
        dist = distance_sensor.get_distance()
        mois = moisture_sensor.moisture
        print(f"Distance: {dist}")
        if mois != MOIS or dist != DIST:
            MOIS = mois
            DIST = dist
            volume = round((math.pi * 56.25 * (24 - dist)) / 1000, 2)
            payload = f"water_test moisture={mois},tank_volume={volume}\n"
            upload_data(payload)
        time.sleep(1)


if __name__ == '__main__':
    main()
