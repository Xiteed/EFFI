import time
import math
from db_handling import upload_data
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
from grove.grove_moisture_sensor import GroveMoistureSensor


MOIS = 0
DIST = 0
TANK_RADIUS = 7.5
TANK_HEIGHT = 24


def measure():
    global MOIS, DIST
    # Moisture sensor should be connected to port PWM.
    # Distance sensor should be connected to port D16.
    moisture_sensor = GroveMoistureSensor(2)
    distance_sensor = GroveUltrasonicRanger(16)

    # Gather sensor data each second and upload them using imported function 'upload_data' if the data has changed.
    while True:
        dist = distance_sensor.get_distance()
        mois = moisture_sensor.moisture
        if mois != MOIS or dist != DIST:
            MOIS = mois
            DIST = dist
            # Calculate the tank volume based on the measured distance and the tank volume + height
            volume = round((math.pi * TANK_RADIUS ^ 2 *
                           (TANK_HEIGHT - dist)) / 1000, 2)
            payload = f'water_resources moisture={mois},tank_volume={volume}\n'
            upload_data(payload)
        time.sleep(1)
