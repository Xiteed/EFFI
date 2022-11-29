import time
from grove.adc import ADC
from db_handling import upload_data
 
__all__ = ["GroveMoistureSensor"]
HUMI = 0

class GroveMoistureSensor:

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()
 
    @property
    def moisture(self):
        value = self.adc.read_voltage(self.channel)
        return value
 
Grove = GroveMoistureSensor
 
def main():
    global MOIS
    sensor = GroveMoistureSensor(2)
    while True:
        mois = sensor.moisture
        if mois != MOIS:
            MOIS = mois
        payload = f"water_test moisture={mois}\n"
        upload_data(payload)
        time.sleep(1)
 
if __name__ == '__main__':
    main()
