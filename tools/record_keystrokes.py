import time
import csv

from pynput import keyboard

FILENAME = 'keystrokes.csv'

# Dictionary to store the keystrokes and their durations
keystrokes = []

# Variable to track the start time of each keystroke
start_time = None

# time of last keystroke
last_release_time = None

# Callback function to handle key press events
def on_press(key):
    global start_time
    global last_release_time

    if start_time is None:
        start_time = time.time()
        if last_release_time is not None:
            duration = round(start_time - last_release_time, 2)
            keystrokes.append(('<pause>', duration))

# Callback function to handle key release events
def on_release(key):
    global start_time
    global last_release_time

    release_time = time.time()
    if start_time is not None:
        duration = round(release_time - start_time, 2)
        keystrokes.append((str(key), duration))
        start_time = None
        last_release_time = release_time

    # Stop the listener if the Escape key is pressed
    if key == keyboard.Key.esc:
        return False

# Create a listener for key events
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Keep the program running until the listener is stopped
listener.join()

with open(FILENAME, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['key','duration'])

    # Write the recorded keystrokes and their durations
    writer.writerows(keystrokes)
