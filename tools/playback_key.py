import csv
import time

import pyautogui

FILENAME = 'keystrokes.csv'

def focus():
    pyautogui.moveTo(200, 275)
    pyautogui.click()

if __name__ == '__main__':
    focus()
    with open(FILENAME, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        prev_key = None
        for key, ms in reader:
            if key == '<pause>':
                if int(ms) < 500:
                    continue

                if prev_key:
                    pyautogui.keyUp(prev_key)

                time.sleep(int(ms)/1000)
            elif len(key) == 1:
                pyautogui.keyDown(key)
                if prev_key:
                    pyautogui.keyUp(prev_key)

                prev_key = key
                time.sleep(int(ms)/1000)

