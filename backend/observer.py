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
    data_json = {}
    with open('user_info.json', 'r') as file:
        data_json = json.loads(file.read())
    tank_level = water_solution.get_current_values()
    max_tank_level = float(data_json['tank_volume'])
    
    # If tank level below 20 % -> warning on display and buzzer sound
    if tank_level / max_tank_level <= 0.2:
        speaker.make_sound()
        display.setText('')
        display.setText('Tank Level Critical: ' + str(tank_level) + 'l')


def check_air_quality():
    humidity = air_quality_solution.get_current_values()['hum']

    # If humidity over 60% and window closed -> warning on display and buzzer sound
    if int(humidity) >= 60 and not is_window_open():
        speaker.make_sound()
        display.setText('')
        display.setText('Air Quality Critical')


def is_window_open():
    with open("window_state.txt", "r") as file:
        if "open" in file.read():
            return True
    return False


if __name__ == '__main__':
    check_air_quality()
    check_tank_level()