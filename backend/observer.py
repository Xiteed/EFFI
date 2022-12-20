import sys
import water_solution
import json
import air_quality_solution

# As the dependencies below can be found in different directories, the python PATH variable needs to be adjusted
sys.path.append('/home/pi20/Documents/EFFI/gpio/actuators')

import display
import speaker

# This file is executed every minute by crontab

def check_tank_level():
    print('Checking Tank level...')
    data_json = {}
    with open('/home/pi20/Documents/EFFI/user_info.json', 'r') as file:
        data_json = json.loads(file.read())
    tank_level = water_solution.get_current_values()
    max_tank_level = float(data_json['tank_volume'])
    print(tank_level, max_tank_level)
    
    # If tank level below 30 % -> warning on display and buzzer sound
    if tank_level / max_tank_level <= 0.3:
        speaker.make_sound()
        display.setText('')
        display.setText('Tank Level Critical: ' + str(tank_level) + 'l')


def check_air_quality():
    print('Checking Air Quality...')
    humidity = air_quality_solution.get_current_values()['hum']

    # If humidity over 60% and window closed -> warning on display and buzzer sound
    if int(humidity) >= 60 and not is_window_open():
        speaker.make_sound()
        display.setText('')
        display.setText('Air Quality Critical: ' + humidity + '%')


def is_window_open():
    with open("/home/pi20/Documents/EFFI/gpio/sensors/window_state.txt", "r") as file:
        if "open" in file.read():
            return True
    return False


if __name__ == '__main__':
    check_air_quality()
    check_tank_level()