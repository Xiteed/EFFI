import time
from grove.adc import ADC
 
__all__ = ["GroveMoistureSensor"]
 
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
    sensor = GroveMoistureSensor(2)
 
    print('Detecting moisture...')
    while True:
        m = sensor.moisture
        if 0 <= m and m < 300:
            result = 'Dry'
        elif 300 <= m and m < 600:
            result = 'Moist'
        else:
            result = 'Wet'
        print('Moisture value: {0}, {1}'.format(m, result))
        time.sleep(1)
 
if __name__ == '__main__':
    main()
