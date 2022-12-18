import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)


def blink():
    GPIO.output(22, True)
    time.sleep(1)
    GPIO.output(22, False)
