import RPi.GPIO as GPIO
import time
import threading
import sys

sys.path.append('/home/pi20/Documents/EFFI/backend')

from window_management import manage_window


GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

light_state = False
application_stopped = False

def switch():
    window_state = ''
    if get_state() == 'closed':
        window_state = 'open'
        window_management = threading.Thread(target=manage_window)
        window_management.start()
    else:
        window_state = 'closed'
    write_state(window_state)


def main():
    try:
        while not application_stopped:
            input_state = GPIO.input(23)
            if input_state == False:
                switch()
                time.sleep(0.2)
    finally:
        GPIO.cleanup()


def get_state():
    with open("/home/pi20/Documents/EFFI/gpio/sensors/window_state.txt", "r") as file:
        if 'open' in file.read():
            return 'open'
    return 'closed'

def write_state(state):
    with open("/home/pi20/Documents/EFFI/gpio/sensors/window_state.txt", "w") as file:
        file.write(state)


if __name__ == "__main__":
    main()
