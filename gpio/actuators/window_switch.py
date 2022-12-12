import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.IN)

window_state = 0
light_state = False


def switch():
    global window_state
    window_state += 1
    write_state()


def main():
    GPIO.output(22, False)
    try:
        while window_state < 2:
            input_state = GPIO.input(23)
            if input_state == False:
                switch()
                time.sleep(0.2)
    finally:
        GPIO.cleanup()


def write_state():
    with open("window_state.txt", "w") as file:
        if window_state == 1:
            file.write("open")
        elif window_state == 2 or window_state == 0:
            file.write("closed")


def light_switch():
    global light_state
    light_state = not light_state
    GPIO.output(22, light_state)


if __name__ == "__main__":
    main()
