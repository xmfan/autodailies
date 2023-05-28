import pyautogui
import time
import csv

FILENAME = 'mousestrokes.csv'

# Function to play back mouse events
def play_mouse_events():
    with open(FILENAME, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for x, y, action, pressed in reader:
            if action == 'move':
                pyautogui.moveTo(float(x), float(y))
            elif action == 'left_click':
                # pyautogui.mouseDown(button='left')
                pass
            elif action == 'right_click':
                # pyautogui.mouseDown(button='right')
                pass

# Start playing back mouse events
play_mouse_events()
