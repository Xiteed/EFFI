import RPi.GPIO as GPIO
import time
import threading
import sys

sys.path.append('/home/pi20/Documents/EFFI/backend')

from window_management import manage_window


GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
application_stopped = False


def switch():
    if not is_open():
        # Window gets opened -> create and start a thread to handle the opened window.
        write_state('open')
        time.sleep(1)
        window_management = threading.Thread(target=manage_window)
        window_management.start()
    else:
        # Window gets closed -> change the state
        # Write the changed window state to the according file to allow other processes to access the window state.
        write_state('closed')


def main():
    while not application_stopped:
        input_state = GPIO.input(23)
        if input_state == False:
            # Button is pressed -> Window state changes
            switch()
            time.sleep(0.2)


def is_open():
    with open("/home/pi20/Documents/EFFI/gpio/sensors/window_state.txt", "r") as file:
        if 'open' in file.read():
            return True
    return False


def write_state(state):
    with open("/home/pi20/Documents/EFFI/gpio/sensors/window_state.txt", "w") as file:
        file.write(state)