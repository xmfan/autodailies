import time
from pynput import keyboard

# Dictionary to store the keystrokes and their durations
keystrokes = []

# Variable to track the start time of each keystroke
start_time = None

# Callback function to handle key press events
def on_press(key):
    global start_time

    if start_time is None:
        start_time = time.time()

# Callback function to handle key release events
def on_release(key):
    global start_time

    if start_time is not None:
        duration = time.time() - start_time
        keystrokes.append((str(key), duration))
        start_time = None

    # Stop the listener if the Escape key is pressed
    if key == keyboard.Key.esc:
        return False

# Create a listener for key events
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Keep the program running until the listener is stopped
listener.join()

# Print the recorded keystrokes and their durations
for key, duration in keystrokes:
    print(f"Key: {key}, Duration: {duration} seconds")
