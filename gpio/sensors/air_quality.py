import time
from seeed_dht import DHT
from grove.adc import ADC
from db_handling import upload_data

HUMI = 0
TEMP = 0
GAS = 0


class GroveGasSensorMQ2:

    def __init__(self):
        self.channel = 1
        self.adc = ADC()

    @property
    def MQ2(self):
        value = self.adc.read(self.channel)
        return value


def measure_air_quality():
    global HUMI, TEMP, GAS
    # Temperature&Humidity sensor should be connected to port D5.
    # Gas sensor should be connected to port A0.
    temphum_sensor = DHT('11', 5)
    gas_sensor = GroveGasSensorMQ2()

    # Gather sensor data each second and upload them using imported function 'upload_data' if the data has changed.
    while True:
        humi, temp = temphum_sensor.read()
        gas = gas_sensor.MQ2
        if humi != HUMI or temp != TEMP or gas != GAS:
            HUMI = humi
            TEMP = temp
            GAS = gas
            payload = f'air_quality temperature={temp},humidity={humi},gas={gas}\n'
            upload_data(payload)
        time.sleep(5)


if __name__ == "__main__":
    measure_air_quality()
