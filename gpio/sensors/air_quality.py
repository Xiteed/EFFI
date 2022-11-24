import time
from seeed_dht import DHT


def measure_temp_hum():  # Grove - Temperature&Humidity Sensor connected to port D5
    sensor = DHT('11', 5)
    while True:
        humi, temp = sensor.read()
        print(f'temperature {temp}C, humidity {humi}%')
        time.sleep(1)


if __name__ == '__main__':
    try:
        measure_temp_hum()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt, cleanup is done")
    finally:
        pwm.stop()
        GPIO.cleanup()
