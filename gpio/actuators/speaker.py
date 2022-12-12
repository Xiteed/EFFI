import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)


def make_sound():
    GPIO.output(24, True)
    time.sleep(0.5)
    GPIO.output(24, False)
