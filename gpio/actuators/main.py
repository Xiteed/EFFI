import time
import speaker
import window_switch
import threading


if __name__ == "__main__":
    buttonThread = threading.Thread(target=window_switch.main)
    buttonThread.start()
    opened = False
    while not opened:
        with open("window_state.txt", "r") as file:
            if "open" in file.read():
                opened = True
                time.sleep(3)
                window_switch.light_switch()
                speaker.make_sound()
    buttonThread.join()
    window_switch.light_switch()
