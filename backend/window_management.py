import time
import sys
from datetime import datetime, timedelta
from air_quality_solution import get_optimal_ventilation_times, is_ventilation_necessary

# As the dependencies below can be found in different directories, the python PATH variable needs to be adjusted
sys.path.append('/home/pi20/Documents/EFFI/gpio/actuators')

import display
import speaker
import light


def manage_window():
    display.setText('')
    display.setText('Window opened.')
    time.sleep(2)
    display.setText('')
    # While the window is open, checks are made regarding the necessity and time of ventilation 
    while is_window_open():
        count = 0
        while is_window_open() and count < 30:
            count += 1
            time.sleep(1)
        ventilation_necessary = is_ventilation_necessary()
        optimal_time_for_ventilation = is_time_optimal()
        handle_window(ventilation_necessary, optimal_time_for_ventilation)
    display.setText('')
    display.setText('Window closed.')
    time.sleep(2)
    display.setText('')


def is_time_optimal():
    # Get the time.
    now = datetime.now().time()
    time_now = datetime.strptime(
        str(now.hour) + ':' + str(now.minute), '%H:%M')

    # Prepare the optimal times.
    optimal_ventilation_times_strings = get_optimal_ventilation_times()
    optimal_ventilation_times = []
    optimal_ventilation_times.append(
        datetime.strptime(optimal_ventilation_times_strings[0], '%H:%M'))
    optimal_ventilation_times.append(
        datetime.strptime(optimal_ventilation_times_strings[2], '%H:%M'))
    if len(optimal_ventilation_times_strings) == 6:
        optimal_ventilation_times.append(
            datetime.strptime(optimal_ventilation_times_strings[4], '%H:%M'))

    # Check whether now is a good time to ventilate.
    for optimal_time in optimal_ventilation_times:
        if time_now >= optimal_time - timedelta(minutes=30) and time_now <= optimal_time + timedelta(minutes=60):
            return True

    return False


def is_window_open():
    with open('/home/pi20/Documents/EFFI/gpio/sensors/window_state.txt', 'r') as file:
        if 'open' in file.read():
            return True
    return False


def handle_window(ventilation_necessary, optimal_time_for_ventilation):
    if not ventilation_necessary:
        # Ventilation is not necessary. -> A warning that the window can be closed is thrown.
        if is_window_open():
            light.blink()
            speaker.make_sound()
            display.setText('')
            display.setText(
                'Vent. unnecess.\nCan be closed.')
    elif ventilation_necessary and not optimal_time_for_ventilation:
        # Ventilation is necessary but outside of optimal times. -> A warning to ventilate carefully is thrown.
        if is_window_open():
            light.blink()
            display.setText('')
            display.setText(
                'Time not optimal\nVent. carefully')
    elif ventilation_necessary and optimal_time_for_ventilation:
        # Ventilation is necessary and inside optimal times.
        count4 = 0
        while is_window_open() and count4 < 270:
            count4 += 1
            time.sleep(1)
        if is_window_open() and not is_ventilation_necessary():
            # If after 5 minutes of ventilation the air quality is suffiently better, recommendation to close the window is shown.
            speaker.make_sound()
            light.blink()
            display.setText('')
            display.setText('Suf. Air Quality\nClose the Window')
        elif is_window_open() and is_ventilation_necessary():
            # If the air quality is still too bad, it gets checked after 5 minutes again.
            count5 = 0
            while is_window_open() and count5 < 300:
                count5 += 1
                time.sleep(1)
            if is_window_open() and not is_ventilation_necessary():
                # If after 5 minutes more of ventilation the air quality is suffiently better, recommendation to close the window is shown.
                speaker.make_sound()
                light.blink()
                display.setText('')
                display.setText('Suf. Air Quality\nClose the Window')
            elif is_window_open() and is_ventilation_necessary:
                display.setText('')
                display.setText(
                    'Air Qual. insuf.\nAvoid Heat loss')
