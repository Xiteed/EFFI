import threading
import sys

sys.path.append('/home/pi20/Documents/EFFI/gpio/sensors')

import air_quality
import water_resource

air_quality_thread = None
water_resource_thread = None


def start():
    global air_quality_thread, water_resource_thread
    air_quality_thread = threading.Thread(target=air_quality.measure_air_quality)
    water_resource_thread = threading.Thread(target=water_resource.measure)
    air_quality.STOP = False
    water_resource.STOP = False
    air_quality_thread.start()
    water_resource_thread.start()
    print("Startup process loading...")


def stop():
    global air_quality_thread, water_resource_thread
    water_resource.STOP = True
    air_quality.STOP = True
    air_quality_thread.join()
    water_resource_thread.join()
    print('Data collecting stopped!')
