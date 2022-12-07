import time
import re


if __name__ == "__main__":
    while True:
        with open("window_state.txt", "r") as file:
            if "open" in file.read():
                time.sleep(3)
                print("please close the window")
                break
