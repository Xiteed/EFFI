import threading
import sys

sys.path.append('/home/pi20/Documents/EFFI/gpio/sensors')

import air_quality
import water_resource
import window_switch

air_quality_thread = None
water_resource_thread = None
window_switch_thread = None

def start():
    global air_quality_thread, water_resource_thread, window_switch_thread
    air_quality_thread = threading.Thread(target=air_quality.measure_air_quality)
    water_resource_thread = threading.Thread(target=water_resource.measure)
    water_switch_thread = threading.Thread(target=window_switch.main)
    air_quality.application_stopped = False
    water_resource.application_stopped = False
    window_switch.application_stopped = False
    air_quality_thread.start()
    water_resource_thread.start()
    water_switch_thread.start()
    print("Startup process loading...")


def stop():
    global air_quality_thread, water_resource_thread
    water_resource.application_stopped = True
    air_quality.application_stopped = True
    window_switch.application_stopped = True
    air_quality_thread.join()
    water_resource_thread.join()
    window_switch_thread.join()
    print('Data collecting stopped!')
