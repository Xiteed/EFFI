import time
from seeed_dht import DHT
from grove.adc import ADC
from db_handling import upload_data

HUMI = 0
TEMP = 0
GAS = 0


class GroveGasSensorMQ2:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def MQ2(self):
        value = self.adc.read(self.channel)
        return value


Grove = GroveGasSensorMQ2


def measure_gas():
    sensor = GroveGasSensorMQ2(0)
    gas = sensor.MQ2
    if gas != GAS:
        GAS = gas
    return GAS


def measure_temp_hum():  # Grove - Temperature&Humidity Sensor connected to port D5
    global HUMI, TEMP, GAS
    temphum_sensor = DHT('11', 5)
    gas_sensor = GroveGasSensorMQ2(0)
    while True:
        humi, temp = temphum_sensor.read()
        gas = gas_sensor.MQ2
        if humi != HUMI or temp != TEMP or gas != GAS:
            HUMI = humi
            TEMP = temp
            GAS = gas
            payload = f"temp_test temperature={temp},humidity={humi},gas={gas}\n"
            upload_data(payload)
        time.sleep(1)


if __name__ == '__main__':
    try:
        measure_temp_hum()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt, cleanup is done")
