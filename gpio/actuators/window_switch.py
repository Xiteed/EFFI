import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.IN)

window_state = False


def switch():
    global window_state
    window_state = not window_state
    write_state()


def main():
    try:
        while True:
            input_state = GPIO.input(25)
            if input_state == False:
                switch()
                GPIO.output(24, window_state)
                time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt, cleaning up GPIOs")
        GPIO.cleanup()


def write_state():
    with open("window_state.txt", "w") as file:
        if window_state:
            file.write("open")
        else:
            file.write("closed")


if __name__ == "__main__":
    main()
